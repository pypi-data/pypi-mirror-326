// src/lib.rs

use pyo3::exceptions::{PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyAny, PyDict};
use numpy::{PyArray1, PyArray2, PyArrayDyn};
use ndarray::{Array1, Array2, ArrayView1, ArrayView2, Axis};
use blas::{sger, dger};
use ndarray_linalg::{Inverse, Solve};
use std::collections::HashMap;

//
// =========================================================================
// Section A. Converter Functions (Py → Rust ndarray)
// =========================================================================

fn convert_any_to_f32_2d<'py>(_py: Python<'py>, obj: &PyAny) -> PyResult<Array2<f32>> {
    let shape: Vec<usize> = obj.getattr("shape")?.extract()?;
    if shape.len() != 2 {
        return Err(PyValueError::new_err("Expected a 2D array for f32"));
    }
    let (nrows, ncols) = (shape[0], shape[1]);
    let dtype_str = obj.getattr("dtype")?.str()?.to_str()?;
    if dtype_str.contains("float32") {
        let arr = obj.downcast::<PyArray2<f32>>()?;
        let view = unsafe { arr.as_array() };
        Ok(view.to_owned())
    } else if dtype_str.contains("float64") {
        let arr = obj.downcast::<PyArrayDyn<f64>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 2 {
            return Err(PyValueError::new_err("Expected 2D float64→f32"));
        }
        let view = view.into_shape((nrows, ncols))
            .map_err(|_| PyValueError::new_err("into_shape fail float64→f32"))?;
        let mut out = Array2::<f32>::zeros((nrows, ncols));
        for i in 0..nrows {
            for j in 0..ncols {
                out[(i, j)] = view[(i, j)] as f32;
            }
        }
        Ok(out)
    } else if dtype_str.contains("int64") {
        let arr = obj.downcast::<PyArrayDyn<i64>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 2 {
            return Err(PyValueError::new_err("Expected 2D int64→f32"));
        }
        let view = view.into_shape((nrows, ncols))
            .map_err(|_| PyValueError::new_err("into_shape fail int64→f32"))?;
        let mut out = Array2::<f32>::zeros((nrows, ncols));
        for i in 0..nrows {
            for j in 0..ncols {
                out[(i, j)] = view[(i, j)] as f32;
            }
        }
        Ok(out)
    } else if dtype_str.contains("int32") {
        let arr = obj.downcast::<PyArrayDyn<i32>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 2 {
            return Err(PyValueError::new_err("Expected 2D int32→f32"));
        }
        let view = view.into_shape((nrows, ncols))
            .map_err(|_| PyValueError::new_err("into_shape fail int32→f32"))?;
        let mut out = Array2::<f32>::zeros((nrows, ncols));
        for i in 0..nrows {
            for j in 0..ncols {
                out[(i, j)] = view[(i, j)] as f32;
            }
        }
        Ok(out)
    } else {
        Err(PyTypeError::new_err("Unsupported 2D dtype for f32"))
    }
}

fn convert_any_to_f32_1d<'py>(_py: Python<'py>, obj: &PyAny) -> PyResult<Array1<f32>> {
    let shape: Vec<usize> = obj.getattr("shape")?.extract()?;
    if shape.len() == 2 && shape[1] == 1 {
        let flat = obj.call_method0("flatten")?;
        return convert_any_to_f32_1d(_py, flat);
    } else if shape.len() != 1 {
        return Err(PyValueError::new_err("Expected 1D array for f32"));
    }
    let dtype_str = obj.getattr("dtype")?.str()?.to_str()?;
    if dtype_str.contains("float32") {
        let arr = obj.downcast::<PyArray1<f32>>()?;
        let view = unsafe { arr.as_array() };
        Ok(view.to_owned())
    } else if dtype_str.contains("float64") {
        let arr = obj.downcast::<PyArrayDyn<f64>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 1 {
            return Err(PyValueError::new_err("Expected 1D float64→f32"));
        }
        let mut out = Array1::<f32>::zeros(view.len());
        for i in 0..view.len() {
            out[i] = view[i] as f32;
        }
        Ok(out)
    } else if dtype_str.contains("int64") {
        let arr = obj.downcast::<PyArrayDyn<i64>>()?;
        let view = unsafe { arr.as_array() };
        let mut out = Array1::<f32>::zeros(view.len());
        for i in 0..view.len() {
            out[i] = view[i] as f32;
        }
        Ok(out)
    } else if dtype_str.contains("int32") {
        let arr = obj.downcast::<PyArrayDyn<i32>>()?;
        let view = unsafe { arr.as_array() };
        let mut out = Array1::<f32>::zeros(view.len());
        for i in 0..view.len() {
            out[i] = view[i] as f32;
        }
        Ok(out)
    } else {
        Err(PyTypeError::new_err("Unsupported dtype for f32 1D"))
    }
}

fn convert_any_to_f64_2d<'py>(_py: Python<'py>, obj: &PyAny) -> PyResult<Array2<f64>> {
    let shape: Vec<usize> = obj.getattr("shape")?.extract()?;
    if shape.len() != 2 {
        return Err(PyValueError::new_err("Expected a 2D array for f64"));
    }
    let (nrows, ncols) = (shape[0], shape[1]);
    let dtype_str = obj.getattr("dtype")?.str()?.to_str()?;
    if dtype_str.contains("float64") {
        let arr = obj.downcast::<PyArray2<f64>>()?;
        let view = unsafe { arr.as_array() };
        Ok(view.to_owned())
    } else if dtype_str.contains("float32") {
        let arr = obj.downcast::<PyArrayDyn<f32>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 2 {
            return Err(PyValueError::new_err("Expected 2D float32→f64"));
        }
        let view = view.into_shape((nrows, ncols))
            .map_err(|_| PyValueError::new_err("into_shape fail float32→f64"))?;
        let mut out = Array2::<f64>::zeros((nrows, ncols));
        for i in 0..nrows {
            for j in 0..ncols {
                out[(i, j)] = view[(i, j)] as f64;
            }
        }
        Ok(out)
    } else if dtype_str.contains("int64") {
        let arr = obj.downcast::<PyArrayDyn<i64>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 2 {
            return Err(PyValueError::new_err("Expected 2D int64→f64"));
        }
        let view = view.into_shape((nrows, ncols))
            .map_err(|_| PyValueError::new_err("into_shape fail int64→f64"))?;
        let mut out = Array2::<f64>::zeros((nrows, ncols));
        for i in 0..nrows {
            for j in 0..ncols {
                out[(i, j)] = view[(i, j)] as f64;
            }
        }
        Ok(out)
    } else if dtype_str.contains("int32") {
        let arr = obj.downcast::<PyArrayDyn<i32>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 2 {
            return Err(PyValueError::new_err("Expected 2D int32→f64"));
        }
        let view = view.into_shape((nrows, ncols))
            .map_err(|_| PyValueError::new_err("into_shape fail int32→f64"))?;
        let mut out = Array2::<f64>::zeros((nrows, ncols));
        for i in 0..nrows {
            for j in 0..ncols {
                out[(i, j)] = view[(i, j)] as f64;
            }
        }
        Ok(out)
    } else {
        Err(PyTypeError::new_err("Unsupported 2D dtype for f64"))
    }
}

fn convert_any_to_f64_1d<'py>(_py: Python<'py>, obj: &PyAny) -> PyResult<Array1<f64>> {
    let shape: Vec<usize> = obj.getattr("shape")?.extract()?;
    if shape.len() == 2 && shape[1] == 1 {
        let flat = obj.call_method0("flatten")?;
        return convert_any_to_f64_1d(_py, flat);
    } else if shape.len() != 1 {
        return Err(PyValueError::new_err("Expected 1D array for f64"));
    }
    let dtype_str = obj.getattr("dtype")?.str()?.to_str()?;
    if dtype_str.contains("float64") {
        let arr = obj.downcast::<PyArray1<f64>>()?;
        let view = unsafe { arr.as_array() };
        Ok(view.to_owned())
    } else if dtype_str.contains("float32") {
        let arr = obj.downcast::<PyArrayDyn<f32>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 1 {
            return Err(PyValueError::new_err("Expected 1D float32→f64"));
        }
        let mut out = Array1::<f64>::zeros(view.len());
        for i in 0..view.len() {
            out[i] = view[i] as f64;
        }
        Ok(out)
    } else if dtype_str.contains("int64") {
        let arr = obj.downcast::<PyArrayDyn<i64>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 1 {
            return Err(PyValueError::new_err("Expected 1D int64→f64"));
        }
        let mut out = Array1::<f64>::zeros(view.len());
        for i in 0..view.len() {
            out[i] = view[i] as f64;
        }
        Ok(out)
    } else if dtype_str.contains("int32") {
        let arr = obj.downcast::<PyArrayDyn<i32>>()?;
        let view = unsafe { arr.as_array() };
        if view.ndim() != 1 {
            return Err(PyValueError::new_err("Expected 1D int32→f64"));
        }
        let mut out = Array1::<f64>::zeros(view.len());
        for i in 0..view.len() {
            out[i] = view[i] as f64;
        }
        Ok(out)
    } else {
        Err(PyTypeError::new_err("Unsupported dtype for f64 1D"))
    }
}

//
// =========================================================================
// Section B. Probit Modules (f32 and f64)
// =========================================================================

mod probit_f32 {
    use super::*;
    use std::f32::consts::{PI, SQRT_2};

    #[inline]
    pub fn erf32(x: f32) -> f32 {
        let a1 = 0.254829592_f32;
        let a2 = -0.284496736_f32;
        let a3 = 1.421413741_f32;
        let a4 = -1.453152027_f32;
        let a5 = 1.061405429_f32;
        let p = 0.3275911_f32;
        let sign = if x < 0.0 { -1.0 } else { 1.0 };
        let x = x.abs();
        let t = 1.0 / (1.0 + p * x);
        let y = 1.0 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * (-x * x).exp();
        sign * y
    }

    #[inline]
    pub fn pdf32(z: f32) -> f32 {
        (-0.5 * z * z).exp() / (2.0 * PI).sqrt()
    }

    #[inline]
    pub fn cdf32(z: f32) -> f32 {
        let val = 0.5 * (1.0 + erf32(z / SQRT_2));
        val.max(1e-15).min(1.0 - 1e-15)
    }

    pub struct ProbitF32<'a> {
        pub endog: ArrayView1<'a, f32>,
        pub exog: ArrayView2<'a, f32>,
        pub weights: Option<ArrayView1<'a, f32>>,
    }

    impl<'a> ProbitF32<'a> {
        pub fn new(
            endog: ArrayView1<'a, f32>,
            exog: ArrayView2<'a, f32>,
            weights: Option<ArrayView1<'a, f32>>,
        ) -> Self {
            ProbitF32 { endog, exog, weights }
        }

        fn w(&self, i: usize) -> f32 {
            self.weights.as_ref().map(|w| w[i]).unwrap_or(1.0)
        }

        pub fn xbeta(&self, params: &ArrayView1<f32>, out: &mut Array1<f32>) {
            *out = self.exog.dot(params);
        }

        pub fn loglike(&self, xbeta: &ArrayView1<f32>) -> f32 {
            let q = self.endog.mapv(|y| 2.0 * y - 1.0);
            let mut sum = 0.0;
            for i in 0..xbeta.len() {
                let z = q[i] * xbeta[i];
                sum += self.w(i) * cdf32(z).ln();
            }
            sum
        }

        pub fn score(&self, xbeta: &ArrayView1<f32>, grad_out: &mut Array1<f32>) {
            grad_out.fill(0.0);
            let n = self.exog.nrows();
            let k = self.exog.ncols();
            let q = self.endog.mapv(|y| 2.0 * y - 1.0);
            for j in 0..k {
                let mut s = 0.0;
                let col = self.exog.column(j);
                for i in 0..n {
                    let z = q[i] * xbeta[i];
                    let pdf = pdf32(z);
                    let cdf = cdf32(z);
                    let ratio = pdf / cdf;
                    let factor = ratio * q[i] * self.w(i);
                    s += col[i] * factor;
                }
                grad_out[j] = s;
            }
        }

        pub fn hessian(&self, xbeta: &ArrayView1<f32>, hess_out: &mut Array2<f32>) {
            hess_out.fill(0.0);
            let (n, k) = self.exog.dim();
            let q = self.endog.mapv(|y| 2.0 * y - 1.0);
            let mut Xw = self.exog.to_owned();
            for i in 0..n {
                let z = q[i] * xbeta[i];
                let pdf = pdf32(z);
                let cdf = cdf32(z);
                let ratio = pdf / cdf;
                let w_i = (ratio * ratio + ratio * z) * self.w(i);
                let sqrt_w = w_i.sqrt();
                for j in 0..k {
                    Xw[(i, j)] *= sqrt_w;
                }
            }
            let tmp = Xw.t().dot(&Xw);
            *hess_out = tmp.mapv(|v| -v);
        }

        pub fn fit_naive_newton(&self, max_iter: usize, tol: f32) -> (Array1<f32>, f32, bool, usize) {
            let k = self.exog.ncols();
            let mut params = Array1::<f32>::zeros(k);
            let mut xbeta = Array1::<f32>::zeros(self.exog.nrows());
            let mut grad = Array1::<f32>::zeros(k);
            let mut hess = Array2::<f32>::zeros((k, k));
            self.xbeta(&params.view(), &mut xbeta);
            let mut ll_old = self.loglike(&xbeta.view());
            let mut converged = false;
            let mut iter_used = 0;
            for iter in 0..max_iter {
                iter_used = iter;
                self.score(&xbeta.view(), &mut grad);
                self.hessian(&xbeta.view(), &mut hess);
                let step = match hess.solve(&grad) {
                    Ok(s) => s,
                    Err(_) => {
                        eprintln!("Hessian singular probit f32 at iter {}", iter);
                        break;
                    }
                };
                for j in 0..k {
                    params[j] -= step[j];
                }
                self.xbeta(&params.view(), &mut xbeta);
                let ll_new = self.loglike(&xbeta.view());
                if (ll_new - ll_old).abs() < tol {
                    converged = true;
                    ll_old = ll_new;
                    break;
                }
                ll_old = ll_new;
            }
            (params, ll_old, converged, iter_used)
        }
    }

    pub fn robust_cov_sger_f32(
        exog: &ArrayView2<f32>,
        xbeta: &ArrayView1<f32>,
        endog: &ArrayView1<f32>,
        weights: Option<&ArrayView1<f32>>,
        h_inv: &ArrayView2<f32>,
        cluster: Option<ArrayView2<f32>>,
    ) -> Array2<f32> {
        let nobs = exog.nrows();
        let kvars = exog.ncols();
        let q = endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta; // Compute z as q * xbeta
        let mut M_flat = vec![0.0_f32; kvars * kvars];
        if let Some(cluster_mat) = cluster {
            if cluster_mat.ncols() != 1 {
                let mut cluster_map: HashMap<u32, Array1<f32>> = HashMap::new();
                for i in 0..nobs {
                    let key = cluster_mat[[i, 0]].to_bits();
                    let q_i = 2.0 * endog[i] - 1.0;
                    // Correct: Use Probit's CDF (cdf32) with z[i]
                    let z_i = q_i * xbeta[i];
                    let p = cdf32(z_i);
                    let score = exog.row(i).to_owned().mapv(|v| v * self_diff_logit(q_i, p));
                    cluster_map
                        .entry(key)
                        .and_modify(|g| *g = g.clone() + score.clone())
                        .or_insert(score);
                }
                for score in cluster_map.values() {
                    unsafe {
                        sger(
                            kvars as i32,
                            kvars as i32,
                            1.0,
                            score.as_slice().unwrap(),
                            1,
                            score.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            } else {
                for i in 0..nobs {
                    // Correct: Use Probit's CDF (cdf32) with z[i]
                    let z_i = q[i] * xbeta[i];
                    let p = cdf32(z_i);
                    let diff = (2.0 * endog[i] - 1.0) - p;
                    let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                    let row = exog.row(i);
                    unsafe {
                        sger(
                            kvars as i32,
                            kvars as i32,
                            factor,
                            row.as_slice().unwrap(),
                            1,
                            row.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            }
        } else {
            for i in 0..nobs {
                // Correct: Use Probit's CDF (cdf32) with z[i]
                let z_i = q[i] * xbeta[i];
                let p = cdf32(z_i);
                let diff = (2.0 * endog[i] - 1.0) - p;
                let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                let row = exog.row(i);
                unsafe {
                    sger(
                        kvars as i32,
                        kvars as i32,
                        factor,
                        row.as_slice().unwrap(),
                        1,
                        row.as_slice().unwrap(),
                        1,
                        &mut M_flat,
                        kvars as i32,
                    );
                }
            }
        }
        let M = Array2::from_shape_vec((kvars, kvars), M_flat)
            .expect("M_flat length error")
            .reversed_axes();
        h_inv.dot(&M).dot(h_inv)
    }

    // Helper: for logit robust covariance we use (y - p) as the score.
    #[inline]
    fn self_diff_logit(y: f32, p: f32) -> f32 {
        y - p
    }
}

mod probit_f64 {
    use super::*;
    use std::f64::consts::{PI, SQRT_2};

    #[inline]
    pub fn erf64(x: f64) -> f64 {
        let a1 = 0.254829592_f64;
        let a2 = -0.284496736_f64;
        let a3 = 1.421413741_f64;
        let a4 = -1.453152027_f64;
        let a5 = 1.061405429_f64;
        let p = 0.3275911_f64;
        let sign = if x < 0.0 { -1.0 } else { 1.0 };
        let x = x.abs();
        let t = 1.0 / (1.0 + p * x);
        let y = 1.0 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * (-x * x).exp();
        sign * y
    }

    #[inline]
    pub fn pdf64(z: f64) -> f64 {
        (-0.5 * z * z).exp() / (2.0 * PI).sqrt()
    }

    #[inline]
    pub fn cdf64(z: f64) -> f64 {
        let val = 0.5 * (1.0 + erf64(z / SQRT_2));
        val.max(1e-15).min(1.0 - 1e-15)
    }

    pub struct ProbitF64<'a> {
        pub endog: ArrayView1<'a, f64>,
        pub exog: ArrayView2<'a, f64>,
        pub weights: Option<ArrayView1<'a, f64>>,
    }

    impl<'a> ProbitF64<'a> {
        pub fn new(
            endog: ArrayView1<'a, f64>,
            exog: ArrayView2<'a, f64>,
            weights: Option<ArrayView1<'a, f64>>,
        ) -> Self {
            ProbitF64 { endog, exog, weights }
        }

        fn w(&self, i: usize) -> f64 {
            self.weights.as_ref().map(|w| w[i]).unwrap_or(1.0)
        }

        pub fn xbeta(&self, params: &ArrayView1<f64>, out: &mut Array1<f64>) {
            *out = self.exog.dot(params);
        }

        pub fn loglike(&self, xbeta: &ArrayView1<f64>) -> f64 {
            let q = self.endog.mapv(|y| 2.0 * y - 1.0);
            let mut sum = 0.0;
            for i in 0..xbeta.len() {
                let z = q[i] * xbeta[i];
                sum += self.w(i) * cdf64(z).ln();
            }
            sum
        }

        pub fn score(&self, xbeta: &ArrayView1<f64>, grad_out: &mut Array1<f64>) {
            grad_out.fill(0.0);
            let n = self.exog.nrows();
            let k = self.exog.ncols();
            let q = self.endog.mapv(|y| 2.0 * y - 1.0);
            for j in 0..k {
                let mut s = 0.0;
                let col = self.exog.column(j);
                for i in 0..n {
                    let z = q[i] * xbeta[i];
                    let pdf = pdf64(z);
                    let cdf = cdf64(z);
                    let ratio = pdf / cdf;
                    let factor = ratio * q[i] * self.w(i);
                    s += col[i] * factor;
                }
                grad_out[j] = s;
            }
        }

        pub fn hessian(&self, xbeta: &ArrayView1<f64>, hess_out: &mut Array2<f64>) {
            hess_out.fill(0.0);
            let (n, k) = self.exog.dim();
            let q = self.endog.mapv(|y| 2.0 * y - 1.0);
            let mut Xw = self.exog.to_owned();
            for i in 0..n {
                let z = q[i] * xbeta[i];
                let pdf = pdf64(z);
                let cdf = cdf64(z);
                let ratio = pdf / cdf;
                let w_i = (ratio * ratio + ratio * z) * self.w(i);
                let sqrt_w = w_i.sqrt();
                for j in 0..k {
                    Xw[(i, j)] *= sqrt_w;
                }
            }
            let tmp = Xw.t().dot(&Xw);
            *hess_out = tmp.mapv(|v| -v);
        }

        pub fn fit_naive_newton(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
            let k = self.exog.ncols();
            let mut params = Array1::<f64>::zeros(k);
            let mut xbeta = Array1::<f64>::zeros(self.exog.nrows());
            let mut grad = Array1::<f64>::zeros(k);
            let mut hess = Array2::<f64>::zeros((k, k));
            self.xbeta(&params.view(), &mut xbeta);
            let mut ll_old = self.loglike(&xbeta.view());
            let mut converged = false;
            let mut iter_used = 0;
            for iter in 0..max_iter {
                iter_used = iter;
                self.score(&xbeta.view(), &mut grad);
                self.hessian(&xbeta.view(), &mut hess);
                let step = match hess.solve(&grad) {
                    Ok(s) => s,
                    Err(_) => {
                        eprintln!("Hessian singular probit f64 at iter {}", iter);
                        break;
                    }
                };
                for j in 0..k {
                    params[j] -= step[j];
                }
                self.xbeta(&params.view(), &mut xbeta);
                let ll_new = self.loglike(&xbeta.view());
                if (ll_new - ll_old).abs() < tol {
                    converged = true;
                    ll_old = ll_new;
                    break;
                }
                ll_old = ll_new;
            }
            (params, ll_old, converged, iter_used)
        }
    }

    pub fn robust_cov_dger_f64(
        exog: &ArrayView2<f64>,
        xbeta: &ArrayView1<f64>,
        endog: &ArrayView1<f64>,
        weights: Option<&ArrayView1<f64>>,
        h_inv: &ArrayView2<f64>,
        cluster: Option<ArrayView2<f64>>,
    ) -> Array2<f64> {
        let nobs = exog.nrows();
        let kvars = exog.ncols();
        let q = endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        let mut M_flat = vec![0.0_f64; kvars * kvars];
        if let Some(cluster_mat) = cluster {
            if cluster_mat.ncols() != 1 {
                let mut cluster_map: HashMap<u64, Array1<f64>> = HashMap::new();
                for i in 0..nobs {
                    let key = cluster_mat[[i, 0]].to_bits();
                    let q_i = 2.0 * endog[i] - 1.0;
                    let z_i = q_i * xbeta[i];
                    let p = cdf64(z_i);
                    let score = exog.row(i).to_owned().mapv(|v| v * self_diff_logit_f64(q_i, p));
                    cluster_map
                        .entry(key)
                        .and_modify(|g| *g += &score)
                        .or_insert(score);
                }
                for score in cluster_map.values() {
                    unsafe {
                        dger(
                            kvars as i32,
                            kvars as i32,
                            1.0,
                            score.as_slice().unwrap(),
                            1,
                            score.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            } else {
                for i in 0..nobs {
                    let z_i = q[i] * xbeta[i];
                    let p = cdf64(z_i);
                    let diff = (2.0 * endog[i] - 1.0) - p;
                    let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                    let row = exog.row(i);
                    unsafe {
                        dger(
                            kvars as i32,
                            kvars as i32,
                            factor,
                            row.as_slice().unwrap(),
                            1,
                            row.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            }
        } else {
            for i in 0..nobs {
                let z_i = q[i] * xbeta[i];
                let p = cdf64(z_i);
                let diff = (2.0 * endog[i] - 1.0) - p;
                let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                let row = exog.row(i);
                unsafe {
                    dger(
                        kvars as i32,
                        kvars as i32,
                        factor,
                        row.as_slice().unwrap(),
                        1,
                        row.as_slice().unwrap(),
                        1,
                        &mut M_flat,
                        kvars as i32,
                    );
                }
            }
        }
        let M = Array2::from_shape_vec((kvars, kvars), M_flat)
            .expect("M_flat length error")
            .reversed_axes();
        h_inv.dot(&M).dot(h_inv)
    }

    #[inline]
    fn self_diff_logit_f64(y: f64, p: f64) -> f64 {
        y - p
    }
}

//

//
// =========================================================================
// Section B2. Logit Modules (f32 and f64)
// =========================================================================

mod logit_f32 {
    use super::*;
    
    #[inline]
    pub fn logistic_cdf32(z: f32) -> f32 {
        1.0 / (1.0 + (-z).exp())
    }

    #[inline]
    pub fn logistic_pdf32(z: f32) -> f32 {
        let cdf = logistic_cdf32(z);
        cdf * (1.0 - cdf)
    }

    pub struct LogitF32<'a> {
        pub endog: ArrayView1<'a, f32>,
        pub exog: ArrayView2<'a, f32>,
        pub weights: Option<ArrayView1<'a, f32>>,
    }

    impl<'a> LogitF32<'a> {
        pub fn new(
            endog: ArrayView1<'a, f32>,
            exog: ArrayView2<'a, f32>,
            weights: Option<ArrayView1<'a, f32>>,
        ) -> Self {
            LogitF32 { endog, exog, weights }
        }

        fn w(&self, i: usize) -> f32 {
            self.weights.as_ref().map(|w| w[i]).unwrap_or(1.0)
        }

        pub fn xbeta(&self, params: &ArrayView1<f32>, out: &mut Array1<f32>) {
            *out = self.exog.dot(params);
        }

        pub fn loglike(&self, xbeta: &ArrayView1<f32>) -> f32 {
            let mut sum = 0.0;
            for i in 0..xbeta.len() {
                let p = logistic_cdf32(xbeta[i]);
                let y = self.endog[i];
                sum += self.w(i) * (y * p.ln() + (1.0 - y) * (1.0 - p).ln());
            }
            sum
        }

        pub fn score(&self, xbeta: &ArrayView1<f32>, grad_out: &mut Array1<f32>) {
            grad_out.fill(0.0);
            let n = self.exog.nrows();
            let k = self.exog.ncols();
            for j in 0..k {
                let mut s = 0.0;
                let col = self.exog.column(j);
                for i in 0..n {
                    let p = logistic_cdf32(xbeta[i]);
                    let diff = self.endog[i] - p;
                    s += col[i] * diff * self.w(i);
                }
                grad_out[j] = s;
            }
        }

        pub fn hessian(&self, xbeta: &ArrayView1<f32>, hess_out: &mut Array2<f32>) {
            hess_out.fill(0.0);
            let (n, k) = self.exog.dim();
            let mut Xw = self.exog.to_owned();
            for i in 0..n {
                let p = logistic_cdf32(xbeta[i]);
                let w_i = p * (1.0 - p) * self.w(i);
                let sqrt_w = w_i.sqrt();
                for j in 0..k {
                    Xw[(i, j)] *= sqrt_w;
                }
            }
            let tmp = Xw.t().dot(&Xw);
            *hess_out = tmp.mapv(|v| -v);
        }

        pub fn fit_naive_newton(&self, max_iter: usize, tol: f32) -> (Array1<f32>, f32, bool, usize) {
            let k = self.exog.ncols();
            let mut params = Array1::<f32>::zeros(k);
            let mut xbeta = Array1::<f32>::zeros(self.exog.nrows());
            let mut grad = Array1::<f32>::zeros(k);
            let mut hess = Array2::<f32>::zeros((k, k));
            self.xbeta(&params.view(), &mut xbeta);
            let mut ll_old = self.loglike(&xbeta.view());
            let mut converged = false;
            let mut iter_used = 0;
            for iter in 0..max_iter {
                iter_used = iter;
                self.score(&xbeta.view(), &mut grad);
                self.hessian(&xbeta.view(), &mut hess);
                let step = match hess.solve(&grad) {
                    Ok(s) => s,
                    Err(_) => {
                        eprintln!("Hessian singular logit f32 at iter {}", iter);
                        break;
                    }
                };
                params += &step;
                self.xbeta(&params.view(), &mut xbeta);
                let ll_new = self.loglike(&xbeta.view());
                if (ll_new - ll_old).abs() < tol {
                    converged = true;
                    ll_old = ll_new;
                    break;
                }
                ll_old = ll_new;
            }
            (params, ll_old, converged, iter_used)
        }
    }

    pub fn robust_cov_logit_f32(
        exog: &ArrayView2<f32>,
        xbeta: &ArrayView1<f32>,
        endog: &ArrayView1<f32>,
        weights: Option<&ArrayView1<f32>>,
        h_inv: &ArrayView2<f32>,
        cluster: Option<ArrayView2<f32>>,
    ) -> Array2<f32> {
        let nobs = exog.nrows();
        let kvars = exog.ncols();
        let mut M_flat = vec![0.0_f32; kvars * kvars];
        
        if let Some(cluster_mat) = cluster {
            if cluster_mat.ncols() != 1 {
                let mut cluster_map: HashMap<u32, Array1<f32>> = HashMap::new();
                for i in 0..nobs {
                    let key = cluster_mat[[i, 0]].to_bits();
                    let p = logistic_cdf32(xbeta[i]);
                    let diff = endog[i] - p;
                    let score = exog.row(i).to_owned().mapv(|v| v * diff * weights.map(|w| w[i]).unwrap_or(1.0));
                    cluster_map.entry(key).and_modify(|g| *g += &score).or_insert(score);
                }
                for score in cluster_map.values() {
                    unsafe {
                        sger(
                            kvars as i32,
                            kvars as i32,
                            1.0,
                            score.as_slice().unwrap(),
                            1,
                            score.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            } else {
                for i in 0..nobs {
                    let p = logistic_cdf32(xbeta[i]);
                    let diff = endog[i] - p;
                    let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                    let row = exog.row(i);
                    unsafe {
                        sger(
                            kvars as i32,
                            kvars as i32,
                            factor,
                            row.as_slice().unwrap(),
                            1,
                            row.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            }
        } else {
            for i in 0..nobs {
                let p = logistic_cdf32(xbeta[i]);
                let diff = endog[i] - p;
                let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                let row = exog.row(i);
                unsafe {
                    sger(
                        kvars as i32,
                        kvars as i32,
                        factor,
                        row.as_slice().unwrap(),
                        1,
                        row.as_slice().unwrap(),
                        1,
                        &mut M_flat,
                        kvars as i32,
                    );
                }
            }
        }
        let M = Array2::from_shape_vec((kvars, kvars), M_flat)
            .expect("M_flat length error")
            .reversed_axes();
        h_inv.dot(&M).dot(h_inv)
    }
}

mod logit_f64 {
    use super::*;

    #[inline]
    pub fn logistic_cdf64(z: f64) -> f64 {
        1.0 / (1.0 + (-z).exp())
    }

    #[inline]
    pub fn logistic_pdf64(z: f64) -> f64 {
        let cdf = logistic_cdf64(z);
        cdf * (1.0 - cdf)
    }

    pub struct LogitF64<'a> {
        pub endog: ArrayView1<'a, f64>,
        pub exog: ArrayView2<'a, f64>,
        pub weights: Option<ArrayView1<'a, f64>>,
    }

    impl<'a> LogitF64<'a> {
        pub fn new(
            endog: ArrayView1<'a, f64>,
            exog: ArrayView2<'a, f64>,
            weights: Option<ArrayView1<'a, f64>>,
        ) -> Self {
            LogitF64 { endog, exog, weights }
        }

        fn w(&self, i: usize) -> f64 {
            self.weights.as_ref().map(|w| w[i]).unwrap_or(1.0)
        }

        pub fn xbeta(&self, params: &ArrayView1<f64>, out: &mut Array1<f64>) {
            *out = self.exog.dot(params);
        }

        pub fn loglike(&self, xbeta: &ArrayView1<f64>) -> f64 {
            let mut sum = 0.0;
            for i in 0..xbeta.len() {
                let p = logistic_cdf64(xbeta[i]);
                let y = self.endog[i];
                sum += self.w(i) * (y * p.ln() + (1.0 - y) * (1.0 - p).ln());
            }
            sum
        }

        pub fn score(&self, xbeta: &ArrayView1<f64>, grad_out: &mut Array1<f64>) {
            grad_out.fill(0.0);
            let n = self.exog.nrows();
            let k = self.exog.ncols();
            for j in 0..k {
                let mut s = 0.0;
                let col = self.exog.column(j);
                for i in 0..n {
                    let p = logistic_cdf64(xbeta[i]);
                    let diff = self.endog[i] - p;
                    s += col[i] * diff * self.w(i);
                }
                grad_out[j] = s;
            }
        }

        pub fn hessian(&self, xbeta: &ArrayView1<f64>, hess_out: &mut Array2<f64>) {
            hess_out.fill(0.0);
            let (n, k) = self.exog.dim();
            let mut Xw = self.exog.to_owned();
            for i in 0..n {
                let p = logistic_cdf64(xbeta[i]);
                let w_i = p * (1.0 - p) * self.w(i);
                let sqrt_w = w_i.sqrt();
                for j in 0..k {
                    Xw[(i, j)] *= sqrt_w;
                }
            }
            let tmp = Xw.t().dot(&Xw);
            *hess_out = tmp.mapv(|v| -v);
        }

        pub fn fit_naive_newton(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
            let k = self.exog.ncols();
            let mut params = Array1::<f64>::zeros(k);
            let mut xbeta = Array1::<f64>::zeros(self.exog.nrows());
            let mut grad = Array1::<f64>::zeros(k);
            let mut hess = Array2::<f64>::zeros((k, k));
            self.xbeta(&params.view(), &mut xbeta);
            let mut ll_old = self.loglike(&xbeta.view());
            let mut converged = false;
            let mut iter_used = 0;
            for iter in 0..max_iter {
                iter_used = iter;
                self.score(&xbeta.view(), &mut grad);
                self.hessian(&xbeta.view(), &mut hess);
                let step = match hess.solve(&grad) {
                    Ok(s) => s,
                    Err(_) => {
                        eprintln!("Hessian singular logit f64 at iter {}", iter);
                        break;
                    }
                };
                params += &step;
                self.xbeta(&params.view(), &mut xbeta);
                let ll_new = self.loglike(&xbeta.view());
                if (ll_new - ll_old).abs() < tol {
                    converged = true;
                    ll_old = ll_new;
                    break;
                }
                ll_old = ll_new;
            }
            (params, ll_old, converged, iter_used)
        }
    }

    pub fn robust_cov_logit_f64(
        exog: &ArrayView2<f64>,
        xbeta: &ArrayView1<f64>,
        endog: &ArrayView1<f64>,
        weights: Option<&ArrayView1<f64>>,
        h_inv: &ArrayView2<f64>,
        cluster: Option<ArrayView2<f64>>,
    ) -> Array2<f64> {
        let nobs = exog.nrows();
        let kvars = exog.ncols();
        let mut M_flat = vec![0.0_f64; kvars * kvars];
        
        if let Some(cluster_mat) = cluster {
            if cluster_mat.ncols() != 1 {
                let mut cluster_map: HashMap<u64, Array1<f64>> = HashMap::new();
                for i in 0..nobs {
                    let key = cluster_mat[[i, 0]].to_bits();
                    let p = logistic_cdf64(xbeta[i]);
                    let diff = endog[i] - p;
                    let score = exog.row(i).to_owned().mapv(|v| v * diff * weights.map(|w| w[i]).unwrap_or(1.0));
                    cluster_map.entry(key).and_modify(|g| *g += &score).or_insert(score);
                }
                for score in cluster_map.values() {
                    unsafe {
                        dger(
                            kvars as i32,
                            kvars as i32,
                            1.0,
                            score.as_slice().unwrap(),
                            1,
                            score.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            } else {
                for i in 0..nobs {
                    let p = logistic_cdf64(xbeta[i]);
                    let diff = endog[i] - p;
                    let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                    let row = exog.row(i);
                    unsafe {
                        dger(
                            kvars as i32,
                            kvars as i32,
                            factor,
                            row.as_slice().unwrap(),
                            1,
                            row.as_slice().unwrap(),
                            1,
                            &mut M_flat,
                            kvars as i32,
                        );
                    }
                }
            }
        } else {
            for i in 0..nobs {
                let p = logistic_cdf64(xbeta[i]);
                let diff = endog[i] - p;
                let factor = weights.map(|ww| ww[i]).unwrap_or(1.0) * diff;
                let row = exog.row(i);
                unsafe {
                    dger(
                        kvars as i32,
                        kvars as i32,
                        factor,
                        row.as_slice().unwrap(),
                        1,
                        row.as_slice().unwrap(),
                        1,
                        &mut M_flat,
                        kvars as i32,
                    );
                }
            }
        }
        let M = Array2::from_shape_vec((kvars, kvars), M_flat)
            .expect("M_flat length error")
            .reversed_axes();
        h_inv.dot(&M).dot(h_inv)
    }
}
// =========================================================================
// Section C. OLS Functions (f32 and f64)
// (They return only coefficients, standard errors, z–scores and p–values.)
// =========================================================================

fn fit_ols_f32(
    exog: &Array2<f32>,
    endog: &Array1<f32>,
    weights: Option<&Array1<f32>>,
    _robust: bool,
    _cluster: Option<&PyAny>,
) -> PyResult<(Array1<f32>, Array1<f32>, Array1<f32>, Array1<f32>)> {
    let n = exog.nrows();
    let k = exog.ncols();
    let w = if let Some(ws) = weights {
        ws.clone()
    } else {
        Array1::ones(n)
    };
    let mut xtw = Array2::<f32>::zeros((k, n));
    for i in 0..n {
        let wi = w[i];
        let row = exog.row(i);
        for j in 0..k {
            xtw[(j, i)] = row[j] * wi;
        }
    }
    let xtwx = exog.t().dot(&xtw);
    let xtwy = exog.t().dot(&(endog * &w));
    let beta = xtwx
        .inv()
        .map_err(|_| PyValueError::new_err("X'WX is singular in OLS f32"))?
        .dot(&xtwy);
    let fitted = exog.dot(&beta);
    let resid = endog - &fitted;
    let sigma2 = (resid.mapv(|v| v * v) * &w).sum() / ((n as f32) - (k as f32));
    let cov = xtwx.inv().unwrap() * sigma2;
    let se = cov.diag().mapv(|v| v.sqrt());
    let z = beta.clone() / &se;
    let p = z.mapv(|z| 2.0 * (1.0 - probit_f32::cdf32(z.abs())));
    Ok((beta, se, z, p))
}

fn fit_ols_f64(
    exog: &Array2<f64>,
    endog: &Array1<f64>,
    weights: Option<&Array1<f64>>,
    _robust: bool,
    _cluster: Option<&PyAny>,
) -> PyResult<(Array1<f64>, Array1<f64>, Array1<f64>, Array1<f64>)> {
    let n = exog.nrows();
    let k = exog.ncols();
    let w = if let Some(ws) = weights {
        ws.clone()
    } else {
        Array1::ones(n)
    };
    let mut xtw = Array2::<f64>::zeros((k, n));
    for i in 0..n {
        let wi = w[i];
        let row = exog.row(i);
        for j in 0..k {
            xtw[(j, i)] = row[j] * wi;
        }
    }
    let xtwx = exog.t().dot(&xtw);
    let xtwy = exog.t().dot(&(endog * &w));
    let beta = xtwx
        .inv()
        .map_err(|_| PyValueError::new_err("X'WX is singular in OLS f64"))?
        .dot(&xtwy);
    let fitted = exog.dot(&beta);
    let resid = endog - &fitted;
    let sigma2 = (resid.mapv(|v| v * v) * &w).sum() / ((n as f64) - (k as f64));
    let cov = xtwx.inv().unwrap() * sigma2;
    let se = cov.diag().mapv(|v| v.sqrt());
    let z = beta.clone() / &se;
    let p = z.mapv(|z| 2.0 * (1.0 - probit_f64::cdf64(z.abs())));
    Ok((beta, se, z, p))
}

//
// =========================================================================
// Section D. Python-Facing Functions
// =========================================================================

#[pyfunction]
fn fit_probit<'py>(
    py: Python<'py>,
    endog_py: &PyAny,
    exog_py: &PyAny,
    max_iter: Option<usize>,
    tol: Option<f32>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
    intercept: Option<bool>,
    precise: Option<bool>,
    weight_var: Option<&PyAny>,
) -> PyResult<&'py PyAny> {
    let use_f64 = precise.unwrap_or(false);
    if !use_f64 {
        let endog = convert_any_to_f32_1d(py, endog_py)?;
        let mut exog = convert_any_to_f32_2d(py, exog_py)?;
        let weights = if let Some(wobj) = weight_var {
            Some(convert_any_to_f32_1d(py, wobj)?)
        } else {
            None
        };
        if intercept.unwrap_or(true) {
            let nobs = exog.nrows();
            let ones = Array2::<f32>::ones((nobs, 1));
            exog = ndarray::concatenate(Axis(1), &[ones.view(), exog.view()])
                .map_err(|e| PyValueError::new_err(format!("Concat intercept probit f32: {}", e)))?;
        }
        let k = exog.ncols();
        let exog_names: Vec<String> = if intercept.unwrap_or(true) {
            let mut names = vec!["Intercept".to_string()];
            for j in 0..(k - 1) {
                names.push(format!("x{}", j));
            }
            names
        } else {
            (0..k).map(|j| format!("x{}", j)).collect()
        };
        let weight_opt: Option<Array1<f32>> = weights.map(|w| w.clone());
        let model = probit_f32::ProbitF32::new(endog.view(), exog.view(), weight_opt.as_ref().map(|w| w.view()));
        let (params, llf, converged, iters) =
            model.fit_naive_newton(max_iter.unwrap_or(30), tol.unwrap_or(1e-6_f32));
        let mut xbeta = Array1::<f32>::zeros(exog.nrows());
        model.xbeta(&params.view(), &mut xbeta);
        let mut hess = Array2::<f32>::zeros((params.len(), params.len()));
        model.hessian(&xbeta.view(), &mut hess);
        let mut cov_final = match hess.inv() {
            Ok(inv) => -inv,
            Err(_) => {
                eprintln!("Hessian singular → identity probit f32");
                -Array2::<f32>::eye(exog.ncols())
            }
        };
        if robust.unwrap_or(false) {
            let cluster_view = if let Some(cv) = cluster_vars {
                let arr = cv.downcast::<PyArray2<f32>>()?;
                let view = unsafe { arr.as_array() };
                if view.nrows() != exog.nrows() {
                    return Err(PyValueError::new_err("Cluster row mismatch probit f32"));
                }
                Some(view)
            } else {
                None
            };
            let h_inv = cov_final.mapv(|x| -x);
            let weight_view = weight_opt.as_ref().map(|w| w.view());
            cov_final = probit_f32::robust_cov_sger_f32(
                &exog.view(),
                &xbeta.view(),
                &endog.view(),
                weight_view.as_ref(),
                &h_inv.view(),
                cluster_view,
            );
        }
        let dict = PyDict::new(py);
        dict.set_item("params", PyArray1::from_owned_array(py, params))?;
        dict.set_item("cov_params", PyArray2::from_owned_array(py, cov_final))?;
        dict.set_item("exog_names", exog_names)?;
        dict.set_item("loglike", llf)?;
        dict.set_item("iterations", iters)?;
        dict.set_item("converged", converged)?;
        dict.set_item("exog", PyArray2::from_owned_array(py, exog))?;
        dict.set_item("endog", PyArray1::from_owned_array(py, endog))?;
        dict.set_item("model_type", "probit")?;
        Ok(dict.into())
    } else {
        let endog = convert_any_to_f64_1d(py, endog_py)?;
        let mut exog = convert_any_to_f64_2d(py, exog_py)?;
        let weights = if let Some(wobj) = weight_var {
            Some(convert_any_to_f64_1d(py, wobj)?)
        } else {
            None
        };
        if intercept.unwrap_or(true) {
            let nobs = exog.nrows();
            let ones = Array2::<f64>::ones((nobs, 1));
            exog = ndarray::concatenate(Axis(1), &[ones.view(), exog.view()])
                .map_err(|e| PyValueError::new_err(format!("Concat intercept probit f64: {}", e)))?;
        }
        let k = exog.ncols();
        let exog_names: Vec<String> = if intercept.unwrap_or(true) {
            let mut names = vec!["Intercept".to_string()];
            for j in 0..(k - 1) {
                names.push(format!("x{}", j));
            }
            names
        } else {
            (0..k).map(|j| format!("x{}", j)).collect()
        };
        let weight_opt: Option<Array1<f64>> = weights.map(|w| w.clone());
        let model = probit_f64::ProbitF64::new(endog.view(), exog.view(), weight_opt.as_ref().map(|w| w.view()));
        let (params, llf, converged, iters) = model.fit_naive_newton(
            max_iter.unwrap_or(30),
            tol.map(|x| x as f64).unwrap_or(1e-6_f64),
        );
        let mut xbeta = Array1::<f64>::zeros(exog.nrows());
        model.xbeta(&params.view(), &mut xbeta);
        let mut hess = Array2::<f64>::zeros((params.len(), params.len()));
        model.hessian(&xbeta.view(), &mut hess);
        let mut cov_final = match hess.inv() {
            Ok(inv) => -inv,
            Err(_) => {
                eprintln!("Hessian singular → identity probit f64");
                -Array2::<f64>::eye(exog.ncols())
            }
        };
        if robust.unwrap_or(false) {
            let cluster_view = if let Some(cv) = cluster_vars {
                let arr = cv.downcast::<PyArray2<f64>>()?;
                let view = unsafe { arr.as_array() };
                if view.nrows() != exog.nrows() {
                    return Err(PyValueError::new_err("Cluster row mismatch probit f64"));
                }
                Some(view)
            } else {
                None
            };
            let h_inv = cov_final.mapv(|x| -x);
            let weight_view = weight_opt.as_ref().map(|w| w.view());
            cov_final = probit_f64::robust_cov_dger_f64(
                &exog.view(),
                &xbeta.view(),
                &endog.view(),
                weight_view.as_ref(),
                &h_inv.view(),
                cluster_view,
            );
        }
        let dict = PyDict::new(py);
        dict.set_item("params", PyArray1::from_owned_array(py, params))?;
        dict.set_item("cov_params", PyArray2::from_owned_array(py, cov_final))?;
        dict.set_item("exog_names", exog_names)?;
        dict.set_item("loglike", llf)?;
        dict.set_item("iterations", iters)?;
        dict.set_item("converged", converged)?;
        dict.set_item("exog", PyArray2::from_owned_array(py, exog))?;
        dict.set_item("endog", PyArray1::from_owned_array(py, endog))?;
        dict.set_item("model_type", "probit")?;
        Ok(dict.into())
    }
}

#[pyfunction]
fn fit_logit<'py>(
    py: Python<'py>,
    endog_py: &PyAny,
    exog_py: &PyAny,
    max_iter: Option<usize>,
    tol: Option<f32>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
    intercept: Option<bool>,
    precise: Option<bool>,
    weight_var: Option<&PyAny>,
) -> PyResult<&'py PyAny> {
    let use_f64 = precise.unwrap_or(false);
    if !use_f64 {
        let endog = convert_any_to_f32_1d(py, endog_py)?;
        let mut exog = convert_any_to_f32_2d(py, exog_py)?;
        let weights = if let Some(wobj) = weight_var {
            Some(convert_any_to_f32_1d(py, wobj)?)
        } else {
            None
        };
        if intercept.unwrap_or(true) {
            let nobs = exog.nrows();
            let ones = Array2::<f32>::ones((nobs, 1));
            exog = ndarray::concatenate(Axis(1), &[ones.view(), exog.view()])
                .map_err(|e| PyValueError::new_err(format!("Concat intercept logit f32: {}", e)))?;
        }
        let k = exog.ncols();
        let exog_names: Vec<String> = if intercept.unwrap_or(true) {
            let mut names = vec!["Intercept".to_string()];
            for j in 0..(k - 1) {
                names.push(format!("x{}", j));
            }
            names
        } else {
            (0..k).map(|j| format!("x{}", j)).collect()
        };
        let weight_opt: Option<Array1<f32>> = weights.map(|w| w.clone());
        let model = logit_f32::LogitF32::new(endog.view(), exog.view(), weight_opt.as_ref().map(|w| w.view()));
        let (params, llf, converged, iters) =
            model.fit_naive_newton(max_iter.unwrap_or(30), tol.unwrap_or(1e-6_f32));
        let mut xbeta = Array1::<f32>::zeros(exog.nrows());
        model.xbeta(&params.view(), &mut xbeta);
        let mut hess = Array2::<f32>::zeros((params.len(), params.len()));
        model.hessian(&xbeta.view(), &mut hess);
        let mut cov_final = match hess.inv() {
            Ok(inv) => -inv,
            Err(_) => {
                eprintln!("Hessian singular → identity logit f32");
                -Array2::<f32>::eye(exog.ncols())
            }
        };
        if robust.unwrap_or(false) {
            let cluster_view = if let Some(cv) = cluster_vars {
                let arr = cv.downcast::<PyArray2<f32>>()?;
                let view = unsafe { arr.as_array() };
                if view.nrows() != exog.nrows() {
                    return Err(PyValueError::new_err("Cluster row mismatch logit f32"));
                }
                Some(view)
            } else {
                None
            };
            let h_inv = cov_final.mapv(|x| -x);
            let weight_view = weight_opt.as_ref().map(|w| w.view());
            // We reuse the robust routine from probit_f32.
            cov_final = logit_f32::robust_cov_logit_f32(
                &exog.view(),
                &xbeta.view(),
                &endog.view(),
                weight_view.as_ref(),
                &h_inv.view(),
                cluster_view,
            );
        }
        let dict = PyDict::new(py);
        dict.set_item("params", PyArray1::from_owned_array(py, params))?;
        dict.set_item("cov_params", PyArray2::from_owned_array(py, cov_final))?;
        dict.set_item("exog_names", exog_names)?;
        dict.set_item("loglike", llf)?;
        dict.set_item("iterations", iters)?;
        dict.set_item("converged", converged)?;
        dict.set_item("exog", PyArray2::from_owned_array(py, exog))?;
        dict.set_item("endog", PyArray1::from_owned_array(py, endog))?;
        dict.set_item("model_type", "logit")?;
        Ok(dict.into())
    } else {
        let endog = convert_any_to_f64_1d(py, endog_py)?;
        let mut exog = convert_any_to_f64_2d(py, exog_py)?;
        let weights = if let Some(wobj) = weight_var {
            Some(convert_any_to_f64_1d(py, wobj)?)
        } else {
            None
        };
        if intercept.unwrap_or(true) {
            let nobs = exog.nrows();
            let ones = Array2::<f64>::ones((nobs, 1));
            exog = ndarray::concatenate(Axis(1), &[ones.view(), exog.view()])
                .map_err(|e| PyValueError::new_err(format!("Concat intercept logit f64: {}", e)))?;
        }
        let k = exog.ncols();
        let exog_names: Vec<String> = if intercept.unwrap_or(true) {
            let mut names = vec!["Intercept".to_string()];
            for j in 0..(k - 1) {
                names.push(format!("x{}", j));
            }
            names
        } else {
            (0..k).map(|j| format!("x{}", j)).collect()
        };
        let weight_opt: Option<Array1<f64>> = weights.map(|w| w.clone());
        let model = logit_f64::LogitF64::new(endog.view(), exog.view(), weight_opt.as_ref().map(|w| w.view()));
        let (params, llf, converged, iters) = model.fit_naive_newton(
            max_iter.unwrap_or(30),
            tol.map(|x| x as f64).unwrap_or(1e-6_f64),
        );
        let mut xbeta = Array1::<f64>::zeros(exog.nrows());
        model.xbeta(&params.view(), &mut xbeta);
        let mut hess = Array2::<f64>::zeros((params.len(), params.len()));
        model.hessian(&xbeta.view(), &mut hess);
        let mut cov_final = match hess.inv() {
            Ok(inv) => -inv,
            Err(_) => {
                eprintln!("Hessian singular → identity logit f64");
                -Array2::<f64>::eye(exog.ncols())
            }
        };
        if robust.unwrap_or(false) {
            let cluster_view = if let Some(cv) = cluster_vars {
                let arr = cv.downcast::<PyArray2<f64>>()?;
                let view = unsafe { arr.as_array() };
                if view.nrows() != exog.nrows() {
                    return Err(PyValueError::new_err("Cluster row mismatch logit f64"));
                }
                Some(view)
            } else {
                None
            };
            let h_inv = cov_final.mapv(|x| -x);
            let weight_view = weight_opt.as_ref().map(|w| w.view());
            cov_final = logit_f64::robust_cov_logit_f64(
                &exog.view(),
                &xbeta.view(),
                &endog.view(),
                weight_view.as_ref(),
                &h_inv.view(),
                cluster_view,
            );
        }
        let dict = PyDict::new(py);
        dict.set_item("params", PyArray1::from_owned_array(py, params))?;
        dict.set_item("cov_params", PyArray2::from_owned_array(py, cov_final))?;
        dict.set_item("exog_names", exog_names)?;
        dict.set_item("loglike", llf)?;
        dict.set_item("iterations", iters)?;
        dict.set_item("converged", converged)?;
        dict.set_item("exog", PyArray2::from_owned_array(py, exog))?;
        dict.set_item("endog", PyArray1::from_owned_array(py, endog))?;
        dict.set_item("model_type", "logit")?;
        Ok(dict.into())
    }
}

#[pyfunction]
fn fit_ols<'py>(
    py: Python<'py>,
    endog_py: &PyAny,
    exog_py: &PyAny,
    intercept: Option<bool>,
    precise: Option<bool>,
    robust: Option<bool>,      // not used in OLS but kept for signature consistency
    cluster_vars: Option<&PyAny>, // not used in OLS
    weight_var: Option<&PyAny>,
) -> PyResult<&'py PyAny> {
    let use_f64 = precise.unwrap_or(false);
    if !use_f64 {
        let endog = convert_any_to_f32_1d(py, endog_py)?;
        let mut exog = convert_any_to_f32_2d(py, exog_py)?;
        let weights = if let Some(wobj) = weight_var {
            Some(convert_any_to_f32_1d(py, wobj)?)
        } else {
            None
        };
        if intercept.unwrap_or(true) {
            let nobs = exog.nrows();
            let ones = Array2::<f32>::ones((nobs, 1));
            exog = ndarray::concatenate(Axis(1), &[ones.view(), exog.view()])
                .map_err(|e| PyValueError::new_err(format!("Concat intercept OLS f32: {}", e)))?;
        }
        let (beta, se, z, p) = fit_ols_f32(&exog, &endog, weights.as_ref(), robust.unwrap_or(false), cluster_vars)?;
        let dict = PyDict::new(py);
        dict.set_item("params", PyArray1::from_owned_array(py, beta))?;
        dict.set_item("Std. Err", PyArray1::from_owned_array(py, se))?;
        dict.set_item("z", PyArray1::from_owned_array(py, z))?;
        dict.set_item("Pr(>|z|)", PyArray1::from_owned_array(py, p))?;
        dict.set_item("model_type", "ols")?;
        dict.set_item("exog", PyArray2::from_owned_array(py, exog))?;
        dict.set_item("endog", PyArray1::from_owned_array(py, endog))?;
        Ok(dict.into())
    } else {
        let endog = convert_any_to_f64_1d(py, endog_py)?;
        let mut exog = convert_any_to_f64_2d(py, exog_py)?;
        let weights = if let Some(wobj) = weight_var {
            Some(convert_any_to_f64_1d(py, wobj)?)
        } else {
            None
        };
        if intercept.unwrap_or(true) {
            let nobs = exog.nrows();
            let ones = Array2::<f64>::ones((nobs, 1));
            exog = ndarray::concatenate(Axis(1), &[ones.view(), exog.view()])
                .map_err(|e| PyValueError::new_err(format!("Concat intercept OLS f64: {}", e)))?;
        }
        let (beta, se, z, p) = fit_ols_f64(&exog, &endog, weights.as_ref(), robust.unwrap_or(false), cluster_vars)?;
        let dict = PyDict::new(py);
        dict.set_item("params", PyArray1::from_owned_array(py, beta))?;
        dict.set_item("Std. Err", PyArray1::from_owned_array(py, se))?;
        dict.set_item("z", PyArray1::from_owned_array(py, z))?;
        dict.set_item("Pr(>|z|)", PyArray1::from_owned_array(py, p))?;
        dict.set_item("model_type", "ols")?;
        dict.set_item("exog", PyArray2::from_owned_array(py, exog))?;
        dict.set_item("endog", PyArray1::from_owned_array(py, endog))?;
        Ok(dict.into())
    }
}

#[pyfunction]
fn ame<'py>(py: Python<'py>, model: &PyAny) -> PyResult<&'py PyAny> {
    // AME applies only to probit and logit models.
    let model_type: String = model.get_item("model_type")?.extract()?;
    if model_type == "ols" {
        return Err(PyValueError::new_err("AME is not applicable for OLS"));
    }
    // For simplicity, we implement AME only for f32 models here.
    ame_f32(py, model)
}

fn ame_f32<'py>(py: Python<'py>, model: &PyAny) -> PyResult<&'py PyAny> {
    use probit_f32::{cdf32, pdf32};
    let params = model.get_item("params")?
        .downcast::<PyArray1<f32>>()?;
    let params_arr = unsafe { params.as_array() }.to_owned();
    let cov = model.get_item("cov_params")?
        .downcast::<PyArray2<f32>>()?;
    let cov_arr = unsafe { cov.as_array() }.to_owned();
    let exog_names: Vec<String> = model.get_item("exog_names")?.extract()?;
    let exog = model.get_item("exog")?
        .downcast::<PyArray2<f32>>()?;
    let exog_arr = unsafe { exog.as_array() };
    let (n, k) = exog_arr.dim();
    let mut intercept_indices = vec![];
    for (ix, name) in exog_names.iter().enumerate() {
        let lower = name.to_lowercase();
        if lower == "intercept" || lower == "const" {
            intercept_indices.push(ix);
        }
    }
    for j in 0..k {
        let col = exog_arr.column(j);
        let first = col[0];
        if col.iter().all(|&v| (v - first).abs() < 1e-12) && !intercept_indices.contains(&j) {
            intercept_indices.push(j);
        }
    }
    let is_discrete: Vec<usize> = (0..k)
        .filter(|&j| {
            if intercept_indices.contains(&j) {
                false
            } else {
                let col = exog_arr.column(j);
                col.iter().all(|&v| v == 0.0 || v == 1.0)
            }
        })
        .collect();
    let z_full = exog_arr.dot(&params_arr);
    let phi_vals = z_full.mapv(|z| pdf32(z));
    let mut sum_ame = vec![0.0_f32; k];
    let mut partial_jl_sums = vec![0.0_f32; k * k];
    for &j in &is_discrete {
        if intercept_indices.contains(&j) {
            continue;
        }
        let beta_j = params_arr[j];
        let col = exog_arr.column(j);
        let delta_j1 = col.mapv(|x| if x == 0.0 { beta_j } else { 0.0 });
        let delta_j0 = col.mapv(|x| if x == 1.0 { -beta_j } else { 0.0 });
        let z_j1 = &z_full + &delta_j1;
        let z_j0 = &z_full + &delta_j0;
        let cdf_j1 = z_j1.mapv(|z| cdf32(z));
        let cdf_j0 = z_j0.mapv(|z| cdf32(z));
        sum_ame[j] += cdf_j1.sum() - cdf_j0.sum();
        let pdf_j1 = z_j1.mapv(|z| pdf32(z));
        let pdf_j0 = z_j0.mapv(|z| pdf32(z));
        let diff_pdf = &pdf_j1 - &pdf_j0;
        for l in 0..k {
            if l == j {
                partial_jl_sums[j * k + l] += pdf_j1.sum();
            } else {
                partial_jl_sums[j * k + l] += diff_pdf.dot(&exog_arr.column(l));
            }
        }
    }
    for j in 0..k {
        if intercept_indices.contains(&j) || is_discrete.contains(&j) {
            continue;
        }
        let beta_j = params_arr[j];
        let sum_phi = phi_vals.sum();
        sum_ame[j] += beta_j * sum_phi;
        let col_sums = exog_arr.sum_axis(Axis(0));
        for l in 0..k {
            let mut val = beta_j * col_sums[l];
            if l == j {
                val += sum_phi;
            }
            partial_jl_sums[j * k + l] += val;
        }
    }
    let ame: Vec<f32> = sum_ame.iter().map(|v| *v / (n as f32)).collect();
    let mut grad_ame = Array2::<f32>::zeros((k, k));
    for j in 0..k {
        for l in 0..k {
            grad_ame[(j, l)] = partial_jl_sums[j * k + l] / (n as f32);
        }
    }
    let cov_ame = grad_ame.dot(&cov_arr).dot(&grad_ame.t());
    let var_ame = cov_ame.diag().mapv(|v| v.max(0.0));
    let se_ame = var_ame.mapv(|v| v.sqrt());
    let add_stars = |p: f32| -> &'static str {
        if p < 0.01 {
            "***"
        } else if p < 0.05 {
            "**"
        } else if p < 0.1 {
            "*"
        } else {
            ""
        }
    };
    let mut dy_dx = Vec::new();
    let mut se_err = Vec::new();
    let mut z_vals = Vec::new();
    let mut p_vals = Vec::new();
    let mut sig = Vec::new();
    for j in 0..k {
        if intercept_indices.contains(&j) {
            continue;
        }
        let val = ame[j];
        let se = se_ame[j];
        let z = if se > 0.0 { val / se } else { f32::NAN };
        let p = 2.0 * (1.0 - cdf32(z.abs()));
        dy_dx.push(val);
        se_err.push(se);
        z_vals.push(z);
        p_vals.push(p);
        sig.push(add_stars(p));
    }
    let pd = py.import("pandas")?;
    let data = PyDict::new(py);
    data.set_item("dy/dx", dy_dx)?;
    data.set_item("Std. Err", se_err)?;
    data.set_item("z", z_vals)?;
    data.set_item("Pr(>|z|)", p_vals)?;
    data.set_item("Significance", sig)?;
    let kwargs = PyDict::new(py);
    kwargs.set_item("data", data)?;
    kwargs.set_item("index", exog_names)?;
    Ok(pd.call_method("DataFrame", (), Some(kwargs))?)
}

//
// =========================================================================
// Section E. Python Module Entry Point
// =========================================================================

#[pymodule]
fn febolt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fit_probit, m)?)?;
    m.add_function(wrap_pyfunction!(fit_logit, m)?)?;
    m.add_function(wrap_pyfunction!(fit_ols, m)?)?;
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    Ok(())
}
