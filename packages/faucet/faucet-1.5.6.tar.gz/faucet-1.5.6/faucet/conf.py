"""Base configuration implementation."""

# Copyright (C) 2015 Brad Cowie, Christopher Lorier and Joe Stringer.
# Copyright (C) 2015 Research and Education Advanced Network New Zealand Ltd.
# Copyright (C) 2015--2017 The Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Conf(object):
    """Base class for FAUCET configuration."""

    defaults = {}
    defaults_types = {}

    def _check_unknown_conf(self, conf):
        """Check that supplied conf dict doesn't specify keys not defined."""
        sub_conf_names = set(conf.keys())
        unknown_conf_names = sub_conf_names - set(self.defaults.keys())
        assert not unknown_conf_names, 'unknown config items: %s' % unknown_conf_names

    def _check_defaults_types(self, conf):
        """Check that conf value is of the correct type."""
        # assert set(list(self.defaults_types.keys())) == set(list(conf.keys()))
        for conf_key, conf_value in list(conf.items()):
            if conf_key in self.defaults_types and conf_value is not None:
                default_type = self.defaults_types[conf_key]
                assert isinstance(conf_value, default_type), '%s value %s must be %s not %s' % (
                    conf_key, conf_value, default_type, type(conf_value))

    def update(self, conf):
        """Parse supplied YAML config and sanity check."""
        self.__dict__.update(conf)
        self._check_unknown_conf(conf)
        self._check_defaults_types(conf)

    def _set_default(self, key, value):
        if key not in self.__dict__ or self.__dict__[key] is None:
            self.__dict__[key] = value

    def to_conf(self):
        """Return configuration as a dict."""
        result = {}
        for k in self.defaults:
            if k != 'name':
                result[k] = self.__dict__[str(k)]
        return result

    def __hash__(self):
        items = [(k, v) for k, v in sorted(list(self.__dict__.items())) if not k.startswith('dyn')]
        return hash(frozenset(list(map(str, items))))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)
