import logging
import posixpath
from os import makedirs, system
from os.path import abspath, expanduser, exists, dirname, join
from shutil import move
from time import perf_counter
import rasters as rt
from rasters import RasterGeometry, Raster
import numpy as np

# Constants for default resampling method, working directory, and download directory
DEFAULT_RESAMPLING = "cubic"
DEFAULT_WORKING_DIRECTORY = "."
DEFAULT_DOWNLOAD_DIRECTORY = "SoilGrids_download"

class SoilGrids:
    """
    A class used to download and process soil data from the Zenodo platform.

    Attributes
    ----------
    FC_URL : str
        URL to the Field Capacity (FC) soil data file on Zenodo.
    WP_URL : str
        URL to the Wilting Point (WP) soil data file on Zenodo.
    logger : Logger
        Logger for logging information.
    working_directory : str
        The working directory for the SoilGrids object.
    source_directory : str
        The source directory for the SoilGrids object.
    resampling : str
        The resampling method for the SoilGrids object.

    Methods
    -------
    __init__(self, working_directory: str = None, source_directory: str = None, resampling: str = DEFAULT_RESAMPLING)
        Initializes the SoilGrids object with a working directory, source directory, and resampling method.
    __repr__(self) -> str
        Returns a string representation of the SoilGrids object.
    FC_filename(self)
        Returns the filename of the field capacity soil data file.
    WP_filename(self)
        Returns the filename of the wilting point soil data file.
    download_file(self, URL: str, filename: str) -> str
        Downloads a file from a given URL to a specified filename.
    FC(self, geometry: RasterGeometry = None, resampling: str = None) -> Raster
        Processes the field capacity soil data file and returns the processed raster.
    WP(self, geometry: RasterGeometry = None, resampling: str = None) -> Raster
        Processes the WP soil data file and returns the processed raster.
    """
    # URLs to specific soil data files on Zenodo
    FC_URL = "https://zenodo.org/record/2784001/files/sol_watercontent.33kPa_usda.4b1c_m_250m_b0..0cm_1950..2017_v0.1.tif"
    WP_URL = "https://zenodo.org/record/2784001/files/sol_watercontent.1500kPa_usda.3c2a1a_m_250m_b0..0cm_1950..2017_v0.1.tif"

    # Logger for logging information
    logger = logging.getLogger(__name__)

    def __init__(self, working_directory: str = None, source_directory: str = None, resampling: str = DEFAULT_RESAMPLING):
        """
        Initializes the SoilGrids object with a working directory, source directory, and resampling method.

        Parameters
        ----------
        working_directory : str, optional
            The working directory for the SoilGrids object (default is None).
        source_directory : str, optional
            The source directory for the SoilGrids object (default is None).
        resampling : str, optional
            The resampling method for the SoilGrids object (default is DEFAULT_RESAMPLING).
        """
        if working_directory is None:
            working_directory = abspath(expanduser(DEFAULT_WORKING_DIRECTORY))

        if source_directory is None:
            source_directory = join(working_directory, DEFAULT_DOWNLOAD_DIRECTORY)

        self.working_directory = abspath(expanduser(working_directory))
        self.source_directory = abspath(expanduser(source_directory))
        self.resampling = resampling

    def __repr__(self) -> str:
        """
        Returns a string representation of the SoilGrids object.

        Returns
        -------
        str
            A string representation of the SoilGrids object.
        """
        return f'SoilGrids(source_directory="{self.source_directory}")'

    @property
    def FC_filename(self):
        """
        Returns the filename of the field capacity soil data file.

        Returns
        -------
        str
            The filename of the field capacity soil data file.
        """
        return join(self.source_directory, posixpath.basename(self.FC_URL))

    @property
    def WP_filename(self):
        """
        Returns the filename of the WP soil data file.

        Returns
        -------
        str
            The filename of the WP soil data file.
        """
        return join(self.source_directory, posixpath.basename(self.WP_URL))

    def download_file(self, URL: str, filename: str) -> str:
        """
        Downloads a file from a given URL to a specified filename.

        Parameters
        ----------
        URL : str
            The URL of the file to download.
        filename : str
            The filename to save the downloaded file as.

        Returns
        -------
        str
            The filename of the downloaded file.
        """
        if exists(filename):
            self.logger.info(f"file already downloaded: {filename}")
            return filename

        self.logger.info(f"downloading: {URL} -> {filename}")
        directory = dirname(filename)
        makedirs(directory, exist_ok=True)
        partial_filename = f"{filename}.download"
        command = f'wget -c -O "{partial_filename}" "{URL}"'
        download_start = perf_counter()
        system(command)
        download_end = perf_counter()
        download_duration = download_end - download_start
        self.logger.info(f"completed download in {download_duration:0.2f} seconds: {filename}")

        if not exists(partial_filename):
            raise IOError(f"unable to download URL: {URL}")

        move(partial_filename, filename)

        return filename

    def FC(self,
           geometry: RasterGeometry = None,
           resampling: str = None) -> Raster:
        """
        Processes the field capacity soil data file and returns the processed raster.

        Parameters
        ----------
        geometry : RasterGeometry, optional
            The geometry to apply to the raster (default is None).
        resampling : str, optional
            The resampling method to use (default is None).

        Returns
        -------
        Raster
            The processed raster.
        """
        if resampling is None:
            resampling = self.resampling

        URL = self.FC_URL
        filename = self.FC_filename

        if not exists(filename):
            self.download_file(URL, filename)

        image = rt.Raster.open(
            filename=filename,
            geometry=geometry,
            resampling=resampling
        )

        image = rt.where(image == 255, np.nan, image)
        image.nodata = np.nan
        image = rt.clip(image / 100, 0, 1)

        return image

    def WP(self,
           geometry: RasterGeometry = None,
           resampling: str = None) -> Raster:
        """
        Processes the wilting point soil data file and returns the processed raster.

        Parameters
        ----------
        geometry : RasterGeometry, optional
            The geometry to apply to the raster (default is None).
        resampling : str, optional
            The resampling method to use (default is None).

        Returns
        -------
        Raster
            The processed raster.
        """
        if resampling is None:
            resampling = self.resampling

        URL = self.WP_URL
        filename = self.WP_filename

        if not exists(filename):
            self.download_file(URL, filename)

        image = rt.Raster.open(
            filename=filename,
            geometry=geometry,
            resampling=resampling
        )

        image = rt.where(image == 255, np.nan, image)
        image.nodata = np.nan
        image = rt.clip(image / 100, 0, 1)

        return image
