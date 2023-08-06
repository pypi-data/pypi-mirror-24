import logging
import os
import shutil
import tempfile
import threading
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal

import docker
import docker.errors

from rundb.client import File
import util


def construct_rundb_file(path, type, host):
    return File(host=host,
                directory=os.path.dirname(path),
                name=os.path.basename(path),
                file_type=type,
                hash="sha512:" + util.sha512_file(path))


DOCKER_ENV = {
    'INPUT_DIR': '/data',
    'OUTPUT_DIR': '/output'
}


class Processor:
    def __init__(self, searcher, rules, hostname):
        """

        :type searcher: rundb.client.RunDbc
        """
        self.hostname = hostname
        self.__rules = rules
        self.rundb = searcher
        self.unproccessed = []
        self.logging = logging.getLogger(self.__class__.__name__)
        self.pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        self.master_pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    def attach_collector(self, collector):
        """

        :type collector: Collector
        """

        def __react_collector(run):
            """

            :type run: RunFiles
            """
            if not run.has_rup():
                return

            run_number = run.run
            self.logging.debug("{}: "
                              "Nominal files {} Actual files {} Has log ? {}".format(run_number, run.n_nominal_files(),
                                                                                     run.n_files(), run.log_file is not None))

            if not run.is_complete():
                return

            self.logging.info("Run {} is complete. Will process. ".format(run_number))

            collector.remove_run(run)

            processed = self.__try_process(run)

            if not processed:
                self.unproccessed.append(run)

        collector.add_observer(__react_collector)

    def set_rules(self, rules):
        self.__rules = rules

        done = []
        for i, run in enumerate(self.unproccessed):
            if self.__try_process(run):
                done.append(i)

        for i in done:
            self.unproccessed.pop(i)

    def __try_process(self, run):
        for rule in self.__rules:
            if rule.matches(run.rup_config):
                self.logging.info("Run {} matches rule {} ".format(run.run, rule.name))
                self.__process(rule, run)
                return True

        self.logging.warn("No rules matching run {}.".format(run.run))
        return False

    def __process(self, rule, run):
        processor = SubProcessor(rule, run, self.rundb, self.hostname, self.pool)

        self.master_pool.submit(processor.process)


class SubProcessor:
    def __init__(self, rule, run, rundb, hostname, pool):
        """

        :type pool: ThreadPoolExecutor
        :type rule: Rule
        :type run: RunFiles
        """
        self.pool = pool
        self.hostname = hostname
        self.logging = logging.getLogger(self.__class__.__name__)
        self.rundb = rundb
        self.run = run
        self.rule = rule
        self.files = run.files
        self.run_number = run.run
        self.rundb_files = []
        self.tmp_raw_files = []
        self.rup_config = run.rup_config
        self.docker = None

    def process(self):
        self.logging.info("Processing {} with rule {}".format(self.run_number, self.rule.name))
        self.__handle_log_file()
        self.__handle_raw_file()
        self.__prepare_docker_image()
        self.__handle_unpacking()
        self.__publish_to_rundb()

    def __handle_log_file(self):
        rup = self.rup_config
        log_dir = self.rule.log_path(rup['experiment'], rup['facility'])

        self.logging.info("mkdir -p {}".format(log_dir))
        util.mkdir_p(log_dir)

        src = self.run.log_file
        dst = os.path.join(log_dir, os.path.basename(src))
        if os.path.exists(dst):
            self.__handle_overwrite(src, dst)
        else:
            shutil.move(src, log_dir)

        self.logging.info("Log file at {}".format(dst))
        self.rundb_files.append(construct_rundb_file(dst, 'log', self.hostname))

    def __handle_raw_file(self):
        rup = self.rup_config
        raw_dir = self.rule.raw_path(rup['experiment'], rup['facility'])

        # Ensuring the raw files are safe
        self.logging.info("mkdir -p {}".format(raw_dir))
        util.mkdir_p(raw_dir)
        self.logging.info("Copying files to RAW dir {}".format(raw_dir))

        def __process(f):
            try:
                base = os.path.basename(f)
                tmp_dst = os.path.join(tempfile.mkdtemp(), base)
                dst = os.path.join(raw_dir, base)

                shutil.copy2(f, tmp_dst)
                self.logging.info("Copied {} to {}".format(base, tmp_dst))

                if f == dst:
                    self.logging.info("{} already in RAW directory. Skipped.".format(base))
                if not os.path.exists(dst):
                    shutil.move(f, raw_dir)
                    self.logging.info("Moved {} to {}".format(base, raw_dir))
                else:
                    self.__handle_overwrite(f, dst)
                    self.logging.info("{} already in correct dir. Skipped.".format(base))

                return tmp_dst, construct_rundb_file(dst, 'raw', self.hostname)

            except Exception as e:
                self.logging.error("Problem with handling {}".format(f))
                self.logging.error(e)
                return None

        for res in self.pool.map(__process, self.files):
            if res is None: continue

            tmp_dst, rundb = res
            self.tmp_raw_files.append(tmp_dst)
            self.rundb_files.append(rundb)

    def __prepare_docker_image(self):
        # Create docker client
        self.docker = docker.from_env()

        # Pull image to ensure up to date
        image = self.rule.image
        try:
            self.docker.images.get(image)
            retries = 1
        except Exception as e:
            self.logging.error(e)
            self.logging.info("Image missing will retry 1000 times")
            retries = 1000

        self.logging.info("Pulling {}".format(self.rule.image))
        for _ in xrange(retries):
            try:
                self.docker.images.pull(self.rule.image)
                break
            except docker.errors.ImageNotFound:
                self.logging.info("Pulling {} failed".format(self.rule.image))
            except Exception as e:
                self.logging.error(e)
            time.sleep(10)

        self.logging.info("Pulling {} - DONE".format(self.rule.image))

    def __handle_unpacking(self):
        unpacked_dir = self.rule.unpacked_path(self.rup_config['experiment'], self.rup_config['facility'])

        self.logging.info("mkdir -p {}".format(unpacked_dir))
        util.mkdir_p(unpacked_dir)

        def __process(f):
            self.logging.info("Processing {}".format(f))
            tmp_output_dir = tempfile.mkdtemp()
            self.logging.debug("Tmp output dir: {}".format(tmp_output_dir))
            res = []

            try:
                tmp_input_dir = os.path.dirname(f)

                # Start image
                image_log = self.docker.containers.run(self.rule.image,
                                           volumes={tmp_input_dir: {'bind': DOCKER_ENV['INPUT_DIR'], 'mode': 'ro'},
                                                    tmp_output_dir: {'bind': DOCKER_ENV['OUTPUT_DIR'], 'mode': 'rw'}},
                                           environment=DOCKER_ENV,
                                           network_mode='none', stdout=True, stderr=True)
                self.logging.info("Log from image ({}):".format(f))
                self.logging.info(image_log)

                self.logging.info("Processing of {} - DONE".format(self.run_number))

                # Move all root files to destination. Delete others
                n_output = 0
                for output in os.listdir(tmp_output_dir):
                    full_f = os.path.join(tmp_output_dir, output)
                    if output.endswith('.root'):
                        src = full_f
                        dst = os.path.join(unpacked_dir, output)
                        self.logging.info("Moving {} to {}".format(src, dst))

                        shutil.move(src, dst)
                        res.append(construct_rundb_file(dst, 'unpacked', self.hostname))
                        n_output += 1
                    else:
                        self.logging.info("Deleting {}".format(full_f))
                        os.remove(full_f)

                if n_output == 0:
                    self.logging.warning("{} produced 0 output files!".format(f))

                # Remove tmp input dir
                shutil.rmtree(tmp_input_dir)

                self.logging.info("Processing {} - DONE".format(f))
            except Exception as e:
                self.logging.error(e)

            for output in os.listdir(tmp_output_dir):
                self.logging.warning("{} is still in put dir! Will delete!".format(output))

            shutil.rmtree(tmp_output_dir)

            return res

        for res in self.pool.map(__process, self.tmp_raw_files):
            for entry in res:
                self.rundb_files.append(entry)
        
    def __publish_to_rundb(self):
        if len(self.rundb_files) == 0:
            self.logging.warning("No files to register for {}".format(self.run_number))
            return

        rup = self.rup_config
        while True:
            try:
                res = self.rundb.search(run_number=self.run_number,
                                        # start_time=rup['start_time'], stop_time=rup['stop_time'],
                                        experiment=rup['experiment'], facility=rup['facility']
                                        )

                if len(res) >= 1:
                    res = res[0]
                    ret = self.rundb.add_files(res.run_id, self.rundb_files)
                    self.logging.info(
                        "Inserted entry for {} with run_id {}. Response: {}".format(self.run_number, res.run_id, ret))
                    break
                else:
                    self.logging.info("No entries for {}. Will wait".format(self.run_number))
            except Exception as e:
                self.logging.error(e)
                pass
            self.logging.info("Publishing {} went wrong. Will retry in 60 seconds".format(self.run_number))
            time.sleep(60)

    def __handle_overwrite(self, src, dst):
        src_sha = util.sha512_file(src)
        dst_sha = util.sha512_file(dst)

        overwrite = None
        if src_sha == dst_sha:
            self.logging.info("Files are identical. Deleting source {}.".format(src))
            os.remove(src)
            overwrite = True
        elif os.stat(src).st_mtime - os.stat(dst).st_mtime > 0:
            self.logging.info("Sources is newer. Overriding".format(src, dst))
            os.rename(src, dst)
            overwrite = True

        return overwrite


def determine_best_match(entries, run):
    """

    :type run: RunFiles
    """
    if entries is None or len(entries) == 0:
        return None

    result = []
    now = datetime.now(tz=tzlocal())
    for x in entries:
        if x.run_number == run.run and x.n_files == run.n_files():
            diff = relativedelta(now, x.timestamp)
            if diff.days < 1:
                result.append(x)

    return result[0] if len(result) > 0 else None
