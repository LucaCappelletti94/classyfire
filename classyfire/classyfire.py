"""Submodule providing the ClassyFire class."""

from typing import Optional, Sequence, Dict, Iterable
import time
import requests
from typeguard import typechecked
from fake_useragent import UserAgent
from cache_decorator import Cache
from tqdm.auto import tqdm
import pandas as pd
from classyfire.exceptions import (
    InvalidInchiKey,
    ClassyFireAPIRequestError,
    InvalidSMILES,
)
from classyfire.utils import (
    is_valid_inchikey,
    is_valid_smiles,
    convert_smiles_to_inchikey,
)
from classyfire.classification import Compound


class ClassyFire:
    """ClassyFire API client."""

    URL = "http://classyfire.wishartlab.com"

    @typechecked
    def __init__(
        self,
        timeout: int = 10,
        sleep: int = 5,
        user_agent: Optional[UserAgent] = None,
        verbose: bool = False,
    ):
        """ClassyFire API client.

        Parameters
        ----------
        timeout : int, optional
            Timeout for the HTTP requests, by default 10
        sleep : int, optional
            Sleep time between requests, by default 5
        user_agent : Optional[UserAgent], optional
            User agent for the HTTP requests, by default None
        verbose : bool, optional
            Whether to print verbose output, by default False
        """
        self._timeout = timeout
        self._sleep = sleep
        self._user_agent: UserAgent = user_agent or UserAgent()
        self._verbose = verbose
        self._last_request_time = 0

    @Cache(
        cache_path="{cache_dir}/{inchikey}.json",
        cache_dir="classyfire_cache",
    )
    @typechecked
    def _classify_inchikey(self, inchikey: str) -> Dict:
        """Get the classification of a chemical entity."""
        inchikey: str = inchikey.replace("InChIKey=", "")
        if not is_valid_inchikey(inchikey):
            raise InvalidInchiKey(inchikey)

        try:
            time_to_sleep = max(
                0, self._sleep - (time.time() - self._last_request_time)
            )
            time.sleep(time_to_sleep)
            self._last_request_time = time.time()
            response = requests.get(
                f"{ClassyFire.URL}/entities/{inchikey}.json",
                timeout=self._timeout,
                headers={
                    "Accept": "application/json",
                    "User-Agent": self._user_agent.chrome,
                },
            )
            response.raise_for_status()

            return response.json()
        except requests.exceptions.HTTPError as e:
            raise ClassyFireAPIRequestError(
                f"Classification request for InChIKey '{inchikey}' failed "
                f"with status code {response.status_code}"
            ) from e
        except requests.exceptions.RequestException as e:
            raise ClassyFireAPIRequestError(
                f"Classification request for InChIKey '{inchikey}' failed"
            ) from e

    @typechecked
    def classify_inchikey(self, inchikey: str) -> Compound:
        """Get the classification of a chemical entity.

        Parameters
        ----------
        inchikey : str
            InChIKey of the chemical entity
        """
        return Compound.from_dict(
            self._classify_inchikey(inchikey),
        )

    @typechecked
    def classify_smiles(self, smiles: str) -> Compound:
        """Get the classification of a chemical entity.

        Parameters
        ----------
        smiles : str
            smiles of the chemical entity
        """
        if not is_valid_smiles(smiles):
            raise InvalidSMILES(smiles)

        return Compound.from_dict(
            self._classify_inchikey(convert_smiles_to_inchikey(smiles)),
        )

    @typechecked
    def classify_inchikeys(self, inchikeys: Sequence[str]) -> Iterable[Compound]:
        """Get the classification of a list of chemical entities.

        Parameters
        ----------
        inchikeys : Sequence[str]
            InChIKeys of the chemical entities
        """
        for inchikey in tqdm(
            inchikeys,
            desc="Classifying InChIKeys",
            unit="InChIKey",
            unit_scale=True,
            leave=False,
            dynamic_ncols=True,
            disable=not self._verbose,
        ):
            yield self.classify_inchikey(inchikey)

    @typechecked
    def classify_smiles_list(self, smiles_list: Sequence[str]) -> Iterable[Compound]:
        """Get the classification of a list of chemical entities.

        Parameters
        ----------
        smiles_list : Sequence[str]
            smiles of the chemical entities
        """
        for smiles in tqdm(
            smiles_list,
            desc="Classifying SMILES",
            unit="SMILES",
            unit_scale=True,
            leave=False,
            dynamic_ncols=True,
            disable=not self._verbose,
        ):
            yield self.classify_smiles(smiles)

    @typechecked
    def classify_csv(
        self, csv_path: str, sep: str = ",", header: bool = True
    ) -> Iterable[Dict[str, Compound]]:
        """Get the classification of a list of chemical entities from a CSV file.

        Parameters
        ----------
        csv_path : str
            Path to the CSV file containing the InChIKeys of the chemical entities
        sep : str, optional
            Separator used in the CSV file, by default ","
        header : bool, optional
            Whether the CSV file contains a header, by default True
        """

        csv_reader = pd.read_csv(
            csv_path, sep=sep, header=0 if header else None, iterator=True, chunksize=1
        )

        for row in tqdm(
            csv_reader,
            desc="Classifying InChIKeys and/or SMILES",
            unit="row",
            unit_scale=True,
            leave=False,
            dynamic_ncols=True,
            disable=not self._verbose,
        ):
            yield {
                column: (
                    self.classify_inchikey(candidate_inchikey_or_smiles)
                    if is_valid_inchikey(candidate_inchikey_or_smiles)
                    else self.classify_smiles(candidate_inchikey_or_smiles)
                )
                for column, candidate_inchikey_or_smiles in row.iloc[0].items()
                if isinstance(candidate_inchikey_or_smiles, str)
                and (
                    is_valid_inchikey(candidate_inchikey_or_smiles)
                    or is_valid_smiles(candidate_inchikey_or_smiles)
                )
            }

    @typechecked
    def classify_df(self, df: pd.DataFrame) -> Iterable[Dict[str, Compound]]:
        """Classify a pandas DataFrame containing InChIKeys and/or SMILES."""

        for _, row in tqdm(
            df.iterrows(),
            desc="Classifying InChIKeys",
            unit="row",
            total=len(df),
            unit_scale=True,
            leave=False,
            dynamic_ncols=True,
            disable=not self._verbose,
        ):
            yield {
                column: (
                    self.classify_inchikey(candidate_inchikey_or_smiles)
                    if is_valid_inchikey(candidate_inchikey_or_smiles)
                    else self.classify_smiles(candidate_inchikey_or_smiles)
                )
                for column, candidate_inchikey_or_smiles in row.items()
                if isinstance(candidate_inchikey_or_smiles, str)
                and (
                    is_valid_inchikey(candidate_inchikey_or_smiles)
                    or is_valid_smiles(candidate_inchikey_or_smiles)
                )
            }
