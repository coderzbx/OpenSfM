import logging
import time

from opensfm import dataset
from opensfm import io
from opensfm import reconstruction

logger = logging.getLogger(__name__)


class Command:
    name = 'merge_reconstruct'
    help = "Merge reconstructions"

    def add_arguments(self, parser):
        parser.add_argument('dataset', help='dataset to process')

    def run(self, args):
        data = None
        start = time.time()
        data_path_str = args.dataset
        data_path_list = str(data_path_str).split(",")
        reconstructions = []
        config = None
        for data_path in data_path_list:
            data = dataset.DataSet(data_path)
            config = data.config
            single_track_reconstructions = data.load_reconstruction()
            for single_reconstruction in single_track_reconstructions:
                reconstructions.append(single_reconstruction)

        reconstructions = reconstruction.merge_reconstructions(reconstructions, config)
        for k, r in enumerate(reconstructions):
            logger.info("Reconstruction {}: {} images, {} points".format(
                k, len(r.shots), len(r.points)))
        logger.info("{} partial reconstructions in total.".format(
            len(reconstructions)))

        end = time.time()

        with open(data.profile_log(), 'a') as fout:
            fout.write('reconstruct: {0}\n'.format(end - start))

        data.save_reconstruction(reconstructions)
