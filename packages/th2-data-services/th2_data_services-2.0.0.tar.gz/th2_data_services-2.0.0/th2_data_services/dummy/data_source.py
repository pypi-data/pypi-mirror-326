#  Copyright 2024-2025 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from th2_data_services.interfaces import IDataSource, ISourceAPI, ICommand


class DummyDataSource(IDataSource):
    """Dummy DataSource.

    Can be useful to create ETCDriver without concrete DataSource or to
    in unit tests.
    """

    def command(self, cmd: ICommand):  # noqa
        raise NotImplementedError

    @property
    def source_api(self) -> ISourceAPI:  # noqa
        raise NotImplementedError
