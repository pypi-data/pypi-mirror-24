# -*- coding: utf-8 -*-
'''
Copyright 2017 by Tobias Houska
This file is part of Statistical Parameter Estimation Tool (SPOTPY).
:author: Benjamin Manns
This module contains a framework to summarize the distance between the model simulations and corresponding observations
by calculating likelihood values.
'''

import numpy as np
import math
import warnings

class LikelihoodError(Exception):
    """
    Define an own error class to know it is an error made by a likelihood calculation to warn the use for wrong inputs
    """
    pass


def __generateMeaserror(data):
    mse = []
    for t in range(data.__len__()):
        # calculate the sd of one data point, i.e. sqrt((dataPointWithError-RealDataPoint)^2)
        mse.append(np.sqrt((data[t] * 2 * 0.1 + data[t] * 2 * 0.1 - data[t]) ** 2))
    return mse


def __calcSimpleDeviation(data, comparedata):
    __standartChecksBeforeStart(data, comparedata)
    d = np.array(data)
    c = np.array(comparedata)
    return d - c


def __standartChecksBeforeStart(data, comparedata):
    # some standard checks
    if data.__len__() != comparedata.__len__():
        raise LikelihoodError("Simulation and observation data have not the same length")
    if data.__len__() == 0:
        raise LikelihoodError("Data with no content can not be used as a foundation of calculation a likelihood")


class TimeSeries:
    """
    The formulae are based on 2002-Brockwell-Introduction Time Series and Forecasting.pdf, pages 17-18
    and is available on every standard statistic literature
    """

    @staticmethod
    def acf(data, lag):
        """
        For a detailed explanation and more background information, please look into "Zeitreihenanalyse", pages 17-18,
        by Matti Schneider, Sebastian Mentemeier, SS 2010

        .. math::

            acf(h) = \\frac{1}{n} \\sum_{t=1}^{n-h}(x_{t+h}-mean(x))(x_t-mean(x))

        :param data: numerical values whereof a acf at lag `h` should be calculated
        :type data: array
        :param lag: lag defines how many steps between each values should be taken to where of a of correlation should be calculated

        :type lag: int
        :return: auto covariation of the data at lag `lag`
        :rtype: float
        """

        len = data.__len__()
        if len <= 0:
            raise LikelihoodError("Data with no content can not be used to calc autokorrelation")
        if lag is None or type(lag) != type(1):
            raise LikelihoodError("The lag musst be an integer")
        if lag > len:
            raise LikelihoodError("The lag can not be bigger then the size of your data")
        m = np.mean(data)
        d = np.array(data)
        # R-Style numpy inline sum
        return np.sum((d[lag:len] - m) * (d[0:len - lag] - m)) / len

    @staticmethod
    def AR_1_Coeff(data):
        """
        The autocovariance coefficient called as rho, for an AR(1) model can be calculated as shown here:

        .. math::

            \\rho(1) = \\frac{\\gamma(1)}{\\gamma(0)}

        For further information look for example in "Zeitreihenanalyse", pages 17, by Matti Schneider, Sebastian Mentemeier,
        SS 2010.

        :param data: numerical array
        :type data: array
        :return: autocorrelation coefficient
        :rtype: float
        """
        return TimeSeries.acf(data, 1) / TimeSeries.acf(data, 0)


class Stats:
    @staticmethod
    def getKyrtosis(data):
        """
        Calculate the forth central moment, see https://de.wikipedia.org/wiki/W%C3%B6lbung_(Statistik)

        :param data: a numerical array
        :type data: array
        :return: the kyrtosis of the data
        :rtype: float
        """
        s = np.std(data)
        n = data.__len__()
        m = np.mean(data)
        npdata = np.array(data)

        return np.sum(((npdata - m) / s) ** 4) / n

    @staticmethod
    def getSkewnessParameter(data):
        """
        Calculate the third central moment, see https://de.wikipedia.org/wiki/Schiefe_(Statistik)

        :param data: a numerical array
        :type data: array
        :return: the skewness of the data
        :rtype: float
        """

        s = np.std(data)
        n = data.__len__()
        m = np.mean(data)
        npdata = np.array(data)
        result = (np.sum(((npdata - m) / s) ** 3) / n)
        if result == 0.0:
            result = 0.001
        return result

def logLikelihood(data, comparedata, measerror=None):
    """
    This formula is based on the gaussian likelihood: homo/heteroscedastic data error formula which can be used in both
    cases if the data has a homo- or heteroscedastic data error. To archive numerical stability a log-transformation was
    done, which derives following formula:

    .. math::

            p = -n/2\\log(2*\\pi)-\\sum_{t=1}^n \\log(\\sigma_t)-0.5*\\sum_{t=1}^n (\\frac{y_t-y_t(x)}{\\sigma_t})^2

    `Usage:` Minimizing the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)
    measerror = np.array(measerror)
    size = measerror[measerror == 0.0].size
    if size > 0:
        warnings.warn("[logLikelihood] reaslized that you use distinct distributed values, that makes no sense at all"
                      "Please use another model for your study. The result will not makes sense.")
        measerror[measerror == 0.0] = np.random.uniform(0.01,0.1,size)


    return -data.__len__()/2*np.log(2*np.pi)-np.sum(np.log(measerror))-0.5*np.sum(((data-comparedata)/measerror)**2)


def gaussianLikelihoodMeasErrorOut(data, comparedata, measerror=None):
    """
    This formular called `Gaussian likelihood: measurement error integrated out` and simply calculates


    .. math::

            p = -n/2\\log(\\sum_{t=1}^n e_t(x)^2)

    with :math:`e_t` is the error residual from `data` and `comparedata`


    `Usage:` The value is always negative, but the "bigger" it is (closer to zero) the better is the fitting.
    So in comparing models, a bigger value leass or equal zero is the goal.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)
    errorArr = np.array(__calcSimpleDeviation(data, comparedata))

    return -data.__len__() / 2 * np.log(np.sum(errorArr ** 2))


def gaussianLikelihoodHomoHeteroDataError(data, comparedata, measerror=None):
    """
    Assuming the data error is normal distributed with zero mean and sigma is the measerror, the standart deviation of
    the meassurment errors
    This formulation allows for homoscedastic (constant variance) and heteroscedastic measuresment errors
    (variance dependent on magnitude of data).

    .. math::

            p = \\prod_{t=1}^{n}\\frac{1}{\\sqrt{2\\pi\\sigma_t^2}}exp(-0.5(\\frac{\\bar y_t - y_t(x) }{sigma_t})^2)


    `Usage:` Minimizing the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    # With the assumption that the error residuals are uncorrelated
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)

    result = 1
    measerror = np.array(measerror)
    measerror[measerror == 0.0] = np.random.uniform(0.1,0.2,[measerror == 0.0].__len__())

    for t in range(data.__len__()):
        likhoodRes = (1 / (np.sqrt(2 * np.pi * measerror[t] ** 2)) * np.exp(
            -0.5 * ((data[t] - comparedata[t]) / (measerror[t])) ** 2))
        if likhoodRes == 0:
            likhoodRes = np.finfo(float).eps ** 2 ** 2 # You can call this a zero or like a hessian would say: 'ebbes'

        result *= likhoodRes
    return result


def LikelihoodAR1WithC(data, comparedata, measerror=None):
    """

    Suppose the error residuals assume an AR(1)-process


    .. math::

            e_t(x)=c+\\phi e_{t-1}(x)+\\eta_t

    with :math:`\\eta_t \\sim N(0,\sigma^2)`, and expectation :math:`E(e_t(x))=c/(1-\\phi)` and variance :math:`\\sigma^2/(1-\\phi^2)`


    This lead to the following standard `log-likelihood`:


    .. math::

            p = -n/2*\\log(2\\pi)-0.5*\\log(\\sigma_1^2/(1-\\phi^2))-\\frac{(e_1(x)-(c/(1-\\phi)))^2}{2\\sigma^2/(1-\\phi^2)}-\\sum_{t=2}^{n}\\log(\\sigma_t)-0.5\\sum_{t=2}^{n}(\\frac{(e_t(x)-c-\\phi e_{t-1}(x))}{\\sigma_t})^2

    `Usage:` Minimizing the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    n = data.__len__()
    if measerror is None:
        measerror = __generateMeaserror(data)

    expect = np.nanmean(data)
    errorArr = np.array(__calcSimpleDeviation(data, comparedata))
    phi = TimeSeries.AR_1_Coeff(data)
    c = expect * (1 - phi)

    # I summarize from 2 to n, but range starts in 1 (in python it is zero index), so just shift it with one
    measerror = np.array(measerror)

    size = measerror[measerror == 0.0]
    if size > 0:
        warnings.warn("[LikelihoodAR1WithC] reaslized that you use distinct distributed values, that makes no sense at all"
                      "Please use another model for your study. The result will not makes sense.")
        measerror[measerror == 0.0] = np.random.uniform(0.01,0.1,size)

    sum_1 = np.sum(np.log(measerror[1:]))

    sum_2 = np.sum(((errorArr[1:] - c - phi * errorArr[:-1]) / (measerror[1:])) ** 2)

    return -(n / 2) * np.log(2 * np.pi) - 0.5 * np.log(measerror[0] ** 2 / (1 - phi ** 2)) - (
        (errorArr[0] - (c / (1 - phi))) ** 2 / (2 * measerror[0] ** 2 / (1 - phi ** 2))) - sum_1 - 0.5 * sum_2


def LikelihoodAR1NoC(data, comparedata, measerror=None):
    """

    Based on the formula in `LikelihoodAR1WithC` we assuming that :math:`c = 0` and that means that the formula of `log-likelihood` is:

    .. math::

            p = -n/2*\\log(2\\pi)+0.5\\log(1-\\phi^2)-0.5(1-\\phi^2)\\sigma_1^{-2}e_1(x)^2-\\sum_{t=2}^{n}\\log(\\sigma_t)-0.5\\sum_{t=2}^{n}(\\frac{e_t(x)-\\phi e_{t-1}(x)}{\\sigma_t})^2

    `Usage:` Minimizing the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    n = data.__len__()
    if measerror is None:
        measerror = __generateMeaserror(data)

    errorArr = np.array(__calcSimpleDeviation(data, comparedata))
    phi = TimeSeries.AR_1_Coeff(data)

    # I summarize from 2 to n, but range starts in 1 (in python it is zero index), so just shift it with one
    measerror = np.array(measerror)
    size = measerror[measerror == 0.0]
    if size > 0:
        warnings.warn(
            "[LikelihoodAR1WithC] reaslized that you use distinct distributed values, that makes no sense at all"
            "Please use another model for your study. The result will not makes sense.")
        measerror[measerror == 0.0] = np.random.uniform(0.01, 0.1, size)

    sum_1 = np.sum(np.log(measerror[1:]))
    sum_2 = np.sum(((errorArr[1:] - phi * errorArr[:-1]) /measerror[1:]) ** 2)


    return -(n / 2) * np.log(2 * np.pi) + 0.5 * np.log(1 - phi ** 2) - 0.5 * (1 - phi ** 2) * (1 / measerror[0] ** 2) * \
                                                                       errorArr[0] ** 2 - sum_1 - 0.5 * sum_2


def generalizedLikelihoodFunction(data, comparedata, measerror=None):
    """
    Under the assumption of having correlated, heteroscedastic, and non‐Gaussian errors and assuming that the data are
    coming from a time series modeled as

    .. math::

            \\Phi_p(B)e_t = \\sigma_t a_t

    with `a_t` is an i.i.d. random error with zero mean and unit standard deviation, described by a skew exponential
    power (SEP) density the likelihood `p` can be calculated as follows:


    .. math::

            p = \\frac{2\\sigma_i}{\\xsi+\\xsi^{-1}}\\omega_\\beta exp(-c_\\beta |a_{\\xsi,t}|^{2/(1+\\beta)})


    where

     .. math::

            a_{\\xsi,t} = \\xsi^{-sign(\\mu_\\xsi+\\sigma_\\xsi a_t )}(\\mu_\\xsi+\\sigma_\\xsi a_t)


    For more detailes see: http://onlinelibrary.wiley.com/doi/10.1029/2009WR008933/epdf, page 3, formualar (6) and pages 15, Appendix A.

    `Usage:` Maximizing the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to
        simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    errorArr = __calcSimpleDeviation(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)
    measerror = np.array(measerror)

    beta = Stats.getKyrtosis(data)

    omegaBeta = np.sqrt(math.gamma(3 * (1 + beta) / 2)) / (1 + beta) * np.sqrt(math.gamma((1 + beta) / 2) ** 3)
    M_1 = math.gamma(1 + beta) / (np.sqrt(math.gamma(3 * (1 + beta) / 2)) * np.sqrt(math.gamma((1 + beta) / 2)))
    M_2 = 1
    xsi = Stats.getSkewnessParameter(data)
    sigma_xsi = np.sqrt(np.abs((M_2 - M_1 ** 2) * (xsi **2 + xsi ** (-2)) + 2 * M_1 ** 2 - M_2))
    cBeta = (math.gamma(3 * (1 + beta) / 2) / math.gamma((1 + beta) / 2)) ** (1 / (1 + beta))

    if xsi != 0.0:
        mu_xsi = M_1 * (xsi - (xsi) ** (-1))
    else:
        mu_xsi = 0.0

    n = data.__len__()

    phi = TimeSeries.AR_1_Coeff(data)

    sum_at = 0
    measerror = np.array(measerror)
    measerror[measerror == 0.0] = np.random.uniform(0.1, 0.2, [measerror == 0.0].__len__())
    for j in range(n - 1):
        t = j + 1
        if t > 0 and t < n and type(t) == type(1):
            a_t = (errorArr[t] - phi * errorArr[t - 1]) / (measerror[t])
        else:

            warnings.warn("Your parameter 't' does not suit to the given data array")
            return None

        a_xsi_t = xsi ** (-1 * np.sign(mu_xsi + sigma_xsi * a_t)) * (mu_xsi + sigma_xsi * a_t)

        sum_at += np.abs(a_xsi_t) ** (2 / (1 + beta))


    return n * np.log(omegaBeta * (2 * sigma_xsi) / np.abs(xsi + (1 / xsi))) - np.sum(
        np.log(measerror)) - cBeta * sum_at


def LaplacianLikelihood(data, comparedata, measerror=None):
    """
    This likelihood function is based on
    https://www.scopus.com/record/display.uri?eid=2-s2.0-0000834243&origin=inward&txGid=cb49b4f37f76ce197f3875d9ea216884
    and use this formula

    .. math::

            p = -\\sum_{t=1}^n \\log(2\\sigma_t)-\\sum_{t=1}^n (\\frac{|e_t(x)|}{\\sigma_t})

    `Usage:` Maximizing the likelihood value guides to the best model, because the less :math:`\\sum_{t=1}^n (\\frac{|e_t(x)|}{\\sigma_t})`
    is the better fits the model simulation data to the observed data.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to
        simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    errArr = np.array(__calcSimpleDeviation(data, comparedata))
    if measerror is None:
        measerror = __generateMeaserror(data)
    measerror = np.array(measerror)

    size = measerror[measerror == 0.0].size
    if size > 0:
        warnings.warn("[LaplacianLikelihood] reaslized that you use distinct distributed values, that makes no sense at all"
                      "Please use another model for your study. The result will not makes sense.")
        measerror[measerror == 0.0] = np.random.uniform(0.01,0.1,size)

    return -1 * np.sum(np.log(2 * measerror)) - np.sum(np.abs(errArr) / measerror)


def SkewedStudentLikelihoodHomoscedastic(data, comparedata, measerror=None):
    """
    Under the assumption that the data are homoscedastic, i.e. the they have a constant measurement error and that the
    residuals :math:`\\epsilon_i` follow a Gaussian distribution we can determine the likelihood by calculation this:

     .. math::

            p = \\prod \\frac{1}{\\sqrt{2\\pi}\\sigma_{const}}exp(-\\frac{\\epsilon_i}{2})

    For detailed mathematical question take a look into hessd-12-2155-2015.pdf
    (https://www.hydrol-earth-syst-sci-discuss.net/12/2155/2015/hessd-12-2155-2015.pdf) pages 2164-2165

    `Usage:` Minimizing the likelihood value guides to the best model. Be aware that only a right model asumption leads to
    a result which makes sense.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: a constant measurement error
    :type measerror: int
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)

    measerror = np.mean(measerror)

    res = np.array(__calcSimpleDeviation(data, comparedata))

    return np.prod(1 / (np.sqrt(2 * np.pi) * measerror) * np.exp(-1 * (res ** 2) / (2)))


def SkewedStudentLikelihoodHeteroscedastic(data, comparedata, measerror=None):
    """
    Under the assumption that the data are heteroscedastic, i.e. the they have for every measurement another error and
    that the residuals are non-Gaussian distributed we perform a likelihoodcalculation based on this formualar, having
    :math:`k` as the skewness parameter from the data and where we assume that the kurtosis parameter :math:`nu > 2`:


     .. math::

            p = \\prod p_i


    Where

    .. math::

            \\eta_i = (\\epsilon_i-\\epsilon_{i-1}\\phi)\\sqrt{1-\\phi^2}

    and

    .. math::

            p_i = \\frac{2c_2\\Gamma(\\frac{\\nu+1}{2})\\sqrt{\\frac{nu}{nu-2}}}{\\Gamma(\\frac{nu}{2})\\sqrt{\\pi \\nu}\\sqrt{1-\\phi^2}\\sigma_i} \\times (1+\\frac{1}{nu-2}(\\frac{c_1+c_2+eta_i}{k^{sign(c_1+c_2+eta_i)}})^2)^{-\\frac{nu+1}{2}}


    and

    .. math::

            c_1 = \\frac{(k^2-\\frac{1}{2})2\\Gamma(\\frac{nu+1}{2})\\sqrt{\\frac{nu}{nu-2}}(nu-2)}{k+\\frac{1}{k}\\Gamma(\\frac{nu}{2})\\sqrt{\\pi nu}(nu-1)}


    and

    .. math::

            c_2 = \\sqrt{-c_1^2+\\frac{k^3+\\frac{1}{k^3}}{k+\\frac{1}{k}}}


    For detailed mathematical question take a look into hessd-12-2155-2015.pdf
    (https://www.hydrol-earth-syst-sci-discuss.net/12/2155/2015/hessd-12-2155-2015.pdf) pages 2165-2169, formular (15).

    `Usage:` Minimizing the likelihood value guides to the best model. Be aware that only a right model asumption leads to
    a result which makes sense.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)

    measerror = np.array(measerror)

    res = np.array(__calcSimpleDeviation(data, comparedata))
    phi = TimeSeries.AR_1_Coeff(res)

    nu = Stats.getKyrtosis(res)
    eta_all = res[1:] - phi * res[:-1] * np.sqrt(1 - phi ** 2)
    k = Stats.getSkewnessParameter(res)

    if nu > 2:

        c_1 = ((k ** 2 - 1 / (k ** 2)) * 2 * math.gamma((nu + 1) / 2) * np.sqrt(nu / (nu - 2)) * (nu - 2)) / (
            (k + (1 / k)) * math.gamma(nu / 2) * np.sqrt(np.pi * nu) * (nu - 1))

        for_c2 = -1 * (c_1) ** 2 + (k ** 3 + 1 / k ** 3) / (k + 1 / k)
        if for_c2 < 0:
            warnings.warn("[SkewedStudentLikelihoodHeteroscedastic]: The correction term c2 is negative and that means that the assumption failed."
                                  "A heteroscedastic skewed student likelihood can not be calculated. We are sorry.")
            return np.NAN
        else:
            c_2 = np.sqrt(for_c2)

        measerror = np.array(measerror)
        size = measerror[measerror == 0.0]
        if size > 0:
            warnings.warn(
                "[SkewedStudentLikelihoodHeteroscedastic] reaslized that you use distinct distributed values, that makes no sense at all"
                "Please use another model for your study. The result will not makes sense.")
            measerror[measerror == 0.0] = np.random.uniform(0.01, 0.1, size)

        return np.prod( (2 * c_2 * math.gamma((nu + 1) / 2) * np.sqrt(nu / (nu - 2))) / (
            (k + 1 / k) * math.gamma(nu / 2) * np.sqrt(np.pi * nu) * np.sqrt(1 - phi ** 2) * measerror[1:]) \
                       * (1 + (1 / (nu - 2)) * (
                           (c_1 + c_2 * eta_all) / (k ** (np.sign(c_1 + c_2 * eta_all)))) ** 2) ** (
                           -(nu + 1) / 2))

    else:
        warnings.warn("[SkewedStudentLikelihoodHeteroscedastic]: The kurtosis parameter is " + str(nu) + " and should be > 2")
        return np.NAN


def SkewedStudentLikelihoodHeteroscedasticAdvancedARModel(data, comparedata, measerror=None):
    """

    This function is based of the previos one, called `SkewedStudentLikelihoodHeteroscedastic`. We expand
    the AR(1) Model so that the expectation of :math:`\\eta_i` is equal to the expectation of a residual :math:`\\epsilon_i`.
    So we having

    .. math::

            \\eta_i = (\\epsilon_i-\\epsilon_{i-1}\\phi + \\frac{\\phi}{N}\\sum_{j = 1}^{N} \\epsilon_j)\\sqrt{1-\\phi^2}

    For detailed mathematical question take a look into hessd-12-2155-2015.pdf
    (https://www.hydrol-earth-syst-sci-discuss.net/12/2155/2015/hessd-12-2155-2015.pdf) pages 2170 formular (20).

    `Usage:` Minimizing the likelihood value guides to the best model. Be aware that only a right model asumption leads to
    a result which makes sense.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)

    measerror = np.array(measerror)
    res = np.array(__calcSimpleDeviation(data, comparedata))
    phi = TimeSeries.AR_1_Coeff(res)
    nu = Stats.getKyrtosis(res)
    N = data.__len__()
    eta_all = (res[1:] - phi * res[:-1] + phi / (N) * np.sum(res)) * np.sqrt(1 - phi ** 2)
    k = Stats.getSkewnessParameter(res)

    if nu > 2:

        c_1 = ((k ** 2 - 1 / (k ** 2)) * 2 * math.gamma((nu + 1) / 2) * np.sqrt(nu / (nu - 2)) * (nu - 2)) / (
            (k + (1 / k)) * math.gamma(nu / 2) * np.sqrt(np.pi * nu) * (nu - 1))

        for_c2 = -1 * (c_1) ** 2 + (k ** 3 + 1 / k ** 3) / (k + 1 / k)
        if for_c2 < 0:
            warnings.warn("[SkewedStudentLikelihoodHeteroscedasticAdvancedARModel]: The correction term c2 is negative and that means that the assumption failed."
                                  "An advanced AR-Model skewed student likelihood can not be calculated. We are sorry.")
            return np.NAN

        else:
            c_2 = np.sqrt(for_c2)

        measerror = np.array(measerror)
        size = measerror[measerror == 0.0]
        if size > 0:
            warnings.warn(
                "[SkewedStudentLikelihoodHeteroscedasticAdvancedARModel] reaslized that you use distinct distributed values, that makes no sense at all"
                "Please use another model for your study. The result will not makes sense.")
            measerror[measerror == 0.0] = np.random.uniform(0.01, 0.1, size)


        return np.prod((2 * c_2 * math.gamma((nu + 1) / 2) * np.sqrt(nu / (nu - 2))) / (
            (k + 1 / k) * math.gamma(nu / 2) * np.sqrt(np.pi * nu) * np.sqrt(1 - phi ** 2) * measerror[1:]) \
                       * (1 + (1 / (nu - 2)) * (
            (c_1 + c_2 * eta_all) / (k ** (np.sign(c_1 + c_2 * eta_all)))) ** 2) ** (
                           -(nu + 1) / 2))


    else:
        warnings.warn("[SkewedStudentLikelihoodHeteroscedasticAdvancedARModel]: The kurtosis parameter is " + str(nu) + " and should be > 2")
        return np.NAN

def NoisyABCGaussianLikelihood(data, comparedata, measerror=None):
    """
    The likelihood function is based on the Wald distribution, whose likelihood function is given by

    .. math::

            p = \\prod_{i=1}^N f(y_i|\\alpha,\\nu).


    A epsilon is used to define :math:`P(\\theta|\\rho(S_1(Y),S_2(Y(X))) < \\epsilon).
    Using the means of the standart observation is a good value for \\epsilon.

    An Euclidean distance calculatino is used, which is based on https://www.reading.ac.uk/web/files/maths/Preprint_MPS_15_09_Prangle.pdf
    , page 2.

    `Usage:` Maximizing the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """

    __standartChecksBeforeStart(data,comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)
    sigmas = np.array(measerror)
    measerror = np.mean(measerror)

    size = sigmas[sigmas == 0.0].size
    if size > 0:
        warnings.warn("[NoisyABCGaussianLikelihood] reaslized that you use distinct distributed values, that makes no sense at all"
                      "Please use another model for your study. The result will not makes sense.")
        sigmas[sigmas == 0.0] = np.random.uniform(0.01,0.1,size)



    m = data.__len__()
    data = np.array(data)
    comparedata = np.array(comparedata)

    # The euclidean distance has a bit diffrent formula then the original paper showed
    return -m/2*np.log(2*np.pi)-m*np.log(measerror)-0.5*1/(measerror**2)* np.sqrt( np.sum( ((data-comparedata)/sigmas)**2 ))



def ABCBoxcarLikelihood(data, comparedata, measerror=None):
    """
    A simple ABC likelihood function is the Boxcar likelihood given by the formular:
    .. math::

            p = \\max{i=1}^N(\\epsilon_j - \\rho(S(Y),S(Y(X)))).


    `Usage:` Minimizing the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)

    data = np.array(data)
    comparedata = np.array(comparedata)

    measerror = np.array(measerror)
    size = measerror[measerror == 0.0].size
    if size > 0:
        warnings.warn("[ABCBoxcarLikelihood] reaslized that you use distinct distributed values, that makes no sense at all"
                      "Please use another model for your study. The result will not makes sense.")
        measerror[measerror == 0.0] = np.random.uniform(0.01,0.1,size)

    # Usage of euclidean distance changes the formula a bit
    return np.min(measerror-np.sqrt(((data-comparedata)/measerror)**2))



def LimitsOfAcceptability(data, comparedata, measerror=None):
    """
   This calculation use the generalized likelihood uncertainty estimation by counting all Euclidean distances which are
   smaller then the deviation of the measurement value.

    .. math::

            p=\\sum_{j=1}^m I(|\\rho(S_j(Y)-S_j(Y(X))| \\leq \\epsilon_j)

    Variable :math:`I(a)` returns one if `a` is true, zero otherwise.

    `Usage:` The bigger the value the better the model returns the observed dataset. Values are all greater equal zero
    and discrete and integer numbers.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param measerror: measurement errors of every data input, if nothing is given a standart calculation is done to simulate measurement errors
    :type measerror: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)
    if measerror is None:
        measerror = __generateMeaserror(data)

    data = np.array(data)
    comparedata = np.array(comparedata)

    measerror = np.array(measerror)
    size = measerror[measerror == 0.0].size
    if size > 0:
        warnings.warn("[LimitsOfAcceptability] reaslized that you use distinct distributed values, that makes no sense at all"
                      "Please use another model for your study. The result will not makes sense.")
        measerror[measerror == 0.0] = np.random.uniform(0.01, 0.1, size)

    # Use simple non euclidean but weighted distance measurement.
    return np.sum(np.abs((data - comparedata) / measerror) <= measerror)


def InverseErrorVarianceShapingFactor(data, comparedata, G=10):
    """
    This function simply use the variance in the error values (:math:`E(X)=Y-Y(X)`) as a likelihood value as this formula
    shows:

    .. math::

            p=-G \\log(\\var(E(x)))

    The factor `G` comes from the DREAMPar model. So this factor can be changed according to the used model.

    For more details see also: http://onlinelibrary.wiley.com/doi/10.1002/hyp.3360060305/epdf.

    `Usage:` Maximize the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param G: DREAMPar model parameter `G`
    :type G: float
    :return: the p value as a likelihood
    :rtype: float
    """

    __standartChecksBeforeStart(data, comparedata)

    errArr = np.array(__calcSimpleDeviation(data, comparedata))

    return -G*np.log(np.nanvar(errArr))


def NashSutcliffeEfficiencyShapingFactor(data, comparedata,G=10):
    """
    This function use the opposite ratio of variance of the error terms between observed and simulated and the variance
    of the observed data as a base to claculate the
    likelihood and transform the values with the logarithm.

    .. math::

            p=G*\\log(1-\\frac{Var(E(x)}{Var(Y)})

    The factor `G` comes from the DREAMPar model. So this factor can be changed according to the used model.

    For more details see also: http://onlinelibrary.wiley.com/doi/10.1029/95WR03723/epdf.

    `Usage:` Maximize the likelihood value guides to the best model. If the function return NAN, than you can not use this
    calculation method or the `comparedata` is too far away from `data`.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param G: DREAMPar model parameter `G`
    :type G: float
    :return: the p value as a likelihood
    :rtype: float
    """

    __standartChecksBeforeStart(data, comparedata)

    errArr = np.array(__calcSimpleDeviation(data, comparedata))

    ratio = np.nanvar(errArr)/np.nanvar(data)

    if ratio > 1:
        warnings.warn("[NashSutcliffeEfficiencyShapingFactor]: The ratio between residual variation and observation "
                      "variation is bigger then one and therefore"
                      "we can not calculate the liklihood. Please use another function which fits to this data and / or "
                      "model")
        return np.NAN
    else:
        return G*np.log(1-ratio)


def ExponentialTransformErrVarShapingFactor(data, comparedata,G=10):
    """
    This function use the variance of the error terms between observed and simulated data as a base to claculate the
    likelihood.

    .. math::

            p=-G*Var(E(x))

    The factor `G` comes from the DREAMPar model. So this factor can be changed according to the used model.

    For more details see also: http://onlinelibrary.wiley.com/doi/10.1029/95WR03723/epdf.

    `Usage:` Maximize the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :param G: DREAMPar model parameter `G`
    :type G: float
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)

    errArr = np.array(__calcSimpleDeviation(data, comparedata))

    return -G*np.nanvar(errArr)

def sumOfAbsoluteErrorResiduals(data, comparedata):
    """
    This function simply calc the deviation between observed and simulated value and perform a log transform. Detailed
    information can be found in http://onlinelibrary.wiley.com/doi/10.1002/hyp.3360060305/epdf.

    .. math::

            p=-\\log(\\sum_{t=1}^n |e_t(x)|)

    `Usage:` Maximize the likelihood value guides to the best model.

    :param data: observed measurements as a numerical array
    :type data: array
    :param comparedata: simulated data from a model which should fit the original data somehow
    :type comparedata: array
    :return: the p value as a likelihood
    :rtype: float
    """
    __standartChecksBeforeStart(data, comparedata)

    errArr = np.array(__calcSimpleDeviation(data,comparedata))

    return -1*np.log(np.sum(np.abs(errArr)))
