# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import pandas as pdt

from mechaphlowers.entities.schemas import (
	CableArrayInput,
	SectionArrayInput,
	WeatherArrayInput,
)


class ElementArray(ABC):
	def __init__(self, data: pdt.DataFrame) -> None:  # type: ignore[arg-type]
		data = self._drop_extra_columns(data)
		self._data: pdt.DataFrame | pd.DataFrame = data  # type: ignore[arg-type]

	@property
	@abstractmethod
	def _input_columns(self) -> list[str]: ...

	def _compute_extra_columns(self, input_data: pdt.DataFrame) -> list[str]:
		return [
			column
			for column in input_data.columns
			if column not in self._input_columns
		]

	def _drop_extra_columns(self, input_data: pdt.DataFrame) -> pdt.DataFrame:
		"""Return a copy of the input pdt.DataFrame, without irrelevant columns.

		Note: This has no impact on the input pdt.DataFrame.
		"""
		extra_columns = self._compute_extra_columns(input_data)
		return input_data.drop(columns=extra_columns)

	def __str__(self) -> str:
		return self._data.to_string()

	def __copy__(self):
		return type(self)(self._data)


class SectionArray(ElementArray):
	"""Description of an overhead line section.

	Args:
	    data: Input data
	    sagging_parameter: Sagging parameter
	    sagging_temperature: Sagging temperature, in Celsius degrees
	"""

	@pa.check_types(lazy=True)
	def __init__(
		self,
		data: pdt.DataFrame[SectionArrayInput] | pd.DataFrame,
		sagging_parameter: float | None = None,
		sagging_temperature: float | None = None,
	) -> None:
		super().__init__(data)  # type: ignore[arg-type]
		self.sagging_parameter = sagging_parameter
		self.sagging_temperature = sagging_temperature

	@property
	def _input_columns(self) -> list[str]:
		metadata = SectionArrayInput.get_metadata()
		return metadata["SectionArrayInput"]["columns"].keys()  # type: ignore

	def compute_elevation_difference(self) -> np.ndarray:
		left_support_height = (
			self._data["conductor_attachment_altitude"]
			- self._data["insulator_length"]
		)
		right_support_height = left_support_height.shift(periods=-1)
		return (right_support_height - left_support_height).to_numpy()

	@property
	def data(self) -> pd.DataFrame:
		if self.sagging_parameter is None or self.sagging_temperature is None:
			raise AttributeError(
				"Cannot return data: sagging_parameter and sagging_temperature are needed"
			)
		else:
			return self._data.assign(
				elevation_difference=self.compute_elevation_difference(),
				sagging_parameter=self.sagging_parameter,
				sagging_temperature=self.sagging_temperature,
			)

	@property
	def data_alone(self) -> pd.DataFrame:
		return self._data.assign(
			elevation_difference=self.compute_elevation_difference()
		)

	def __copy__(self):
		copy_obj = super().__copy__()
		copy_obj.sagging_parameter = self.sagging_parameter
		copy_obj.sagging_temperature = self.sagging_temperature
		return copy_obj


class CableArray(ElementArray):
	"""Physical description of a cable.

	Args:
		data: Input data
	"""

	@pa.check_types(lazy=True)
	def __init__(
		self,
		data: pdt.DataFrame[CableArrayInput] | pd.DataFrame,
	) -> None:
		super().__init__(data)  # type: ignore[arg-type]

	@property
	def _input_columns(self) -> list[str]:
		metadata = CableArrayInput.get_metadata()
		return metadata["CableArrayInput"]["columns"].keys()  # type: ignore

	@property
	def data(self) -> pd.DataFrame:
		data_SI = self._data.copy()
		data_SI["section"] *= 1e-6
		data_SI["diameter"] *= 1e-3
		data_SI["young_modulus"] *= 1e9
		data_SI["dilatation_coefficient"] *= 1e-6
		return data_SI

	@property
	def data_original_units(self) -> pd.DataFrame:
		return self._data


class WeatherArray(ElementArray):
	"""Weather-related data, such as wind and ice.

	They're typically used to compute weather-related loads on the cable.
	"""

	@pa.check_types(lazy=True)
	def __init__(
		self,
		data: pdt.DataFrame[WeatherArrayInput] | pd.DataFrame,
	) -> None:
		super().__init__(data)  # type: ignore[arg-type]

	@property
	def _input_columns(self) -> list[str]:
		metadata = WeatherArrayInput.get_metadata()
		return metadata["WeatherArrayInput"]["columns"].keys()  # type: ignore

	@property
	def data(self) -> pd.DataFrame:
		data_SI = self._data.copy()
		data_SI["ice_thickness"] *= 1e-2
		return data_SI

	@property
	def data_original_units(self) -> pd.DataFrame:
		return self._data
