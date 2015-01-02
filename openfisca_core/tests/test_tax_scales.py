# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np

from openfisca_core.taxscales import MarginalRateTaxScale
from openfisca_core.tools import assert_near


def test_linear_average_rate_tax_scale():
    base = np.array([1, 1.5, 2, 2.5])

    marginal_tax_scale = MarginalRateTaxScale()
    marginal_tax_scale.add_bracket(0, 0)
    marginal_tax_scale.add_bracket(1, 0.1)
    marginal_tax_scale.add_bracket(2, 0.2)
    assert_near(marginal_tax_scale.calc(base), [0, .05, .1, .2], error_margin = 0)

    average_tax_scale = marginal_tax_scale.to_average()
    assert_near(average_tax_scale.thresholds, [0, 1, 2, np.inf], error_margin = 0)
    assert_near(average_tax_scale.rates, [0, 0, 0.05, 0.2], error_margin = 0)
    assert_near(average_tax_scale.calc(base), [0, 0.0375, 0.1, 0.125], error_margin = 1e-10)

    new_marginal_tax_scale = average_tax_scale.to_marginal()
    assert_near(new_marginal_tax_scale.thresholds, marginal_tax_scale.thresholds, error_margin = 0)
    assert_near(new_marginal_tax_scale.rates, marginal_tax_scale.rates, error_margin = 0)
    assert_near(average_tax_scale.rates, [0, 0, 0.05, 0.2], error_margin = 0)