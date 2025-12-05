import numpy as np


TOL_ERRO_FINAL = 1e-2 
MIN_ITER = 1 
MAX_ITER = 10 
MIN_DIV = 1e-12 

def cgnr(H: np.ndarray, g: np.ndarray, max_iterations: int = MAX_ITER, tol: float = TOL_ERRO_FINAL, min_iterations: int = MIN_ITER, lambda_reg: float = 0.0, logger=None) -> tuple:
    m, n = H.shape
    f = np.zeros((n, 1))
    g = g.reshape(-1, 1)
    
    r = g - H @ f
    z = H.T @ r
    p = z.copy()
    
    initial_residual_norm = np.linalg.norm(r)
    number_iterations = 0

    if logger is not None:
        logger.info(f"CGNR: tol={tol:.3e}")

    for i in range(max_iterations):
        w = H @ p
        z_dot = float(z.T @ z)
        
        w_dot = float(w.T @ w) + MIN_DIV
        alpha = z_dot / w_dot
        
        f_new = f + alpha * p
        r_new = r - alpha * w
        z_new = H.T @ r_new
        z_new_dot = float(z_new.T @ z_new)
        
        beta_den = z_dot + MIN_DIV
        beta = z_new_dot / beta_den
        
        p_new = z_new + beta * p

        current_residual_norm = np.linalg.norm(r_new)
        relative_error = current_residual_norm / (initial_residual_norm + MIN_DIV)

        if logger is not None:
            logger.info(
                f"Iteracao {i + 1}: erro relativo = {relative_error:.6e}, residuo = {current_residual_norm:.3e}"
            )

        f, r, z, p = f_new, r_new, z_new, p_new
        number_iterations = i + 1

        # o erro deve ser menor que a tolerancia de 1e-2
        if number_iterations >= min_iterations and relative_error < tol:
            if logger is not None:
                logger.info(f"Convergiu com erro relativo {relative_error:.2e} < {tol:.2e}")
            break

    final_residual = g - H @ f
    final_error = np.linalg.norm(final_residual) / (np.linalg.norm(g) + MIN_DIV)
    return f.flatten(), number_iterations, final_error

def cgne(H: np.ndarray, g: np.ndarray, max_iterations: int = MAX_ITER, tol: float = TOL_ERRO_FINAL, min_iterations: int = MIN_ITER, reg_factor: float = 0.0, logger=None) -> tuple:
    N = H.shape[1]
    f = np.zeros((N, 1))
    g = g.reshape(-1, 1)
    r = g - H @ f
    p = H.T @ r
    initial_residual_norm = np.linalg.norm(r)
    min_div = 1e-12
    final_iterations = 0

    if logger is not None:
        logger.info(f"CGNE: tol={tol:.3e}")

    for i in range(max_iterations):
        Hp = H @ p
        alpha_num = float(r.T @ r)
        alpha_den = float(Hp.T @ Hp) + min_div
        if alpha_den < min_div:
            break
        alpha = alpha_num / alpha_den
        f_new = f + alpha * p
        r_new = r - alpha * (H @ p)
        beta_num = float(r_new.T @ r_new)
        beta_den = float(r.T @ r) + min_div
        beta = beta_num / beta_den
        p_new = H.T @ r_new + beta * p

        current_residual_norm = np.linalg.norm(r_new)
        relative_error = current_residual_norm / (initial_residual_norm + min_div)

        if logger is not None:
            logger.info(f"Iteracao {i + 1}: erro relativo = {relative_error:.6e}")

        f, r, p = f_new, r_new, p_new
        final_iterations = i + 1

        if final_iterations >= min_iterations and relative_error < tol:
            if logger is not None:
                logger.info(f"Convergiu com erro relativo {relative_error:.2e} < {tol:.2e}")
            break

    final_error = np.linalg.norm(g - H @ f) / (np.linalg.norm(g) + min_div)
    return f.flatten(), final_iterations, final_error