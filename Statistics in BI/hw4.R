print_intervals <- function(seq, conf_level, m, std_dev)
{
  d_f = length(seq) - 1

  disp = qt(prob_level, d_f) * std_dev / sqrt(length(seq))
  
  left_disp = d_f * std_dev ** 2 / qchisq((1 + conf_level) / 2, df = d_f)
  right_disp = d_f * std_dev ** 2 / qchisq((1 - conf_level) / 2, df = d_f)

  cat("Mean: ", m, "; interval: (", m - disp, " - ", m + disp, ")\n")
  cat("Dispersion: ", std_dev ** 2, "; interval: (", left_disp, " - ", right_disp, ")\n")
}

seq1 <- c(-1.24, -0.75, 0.82, 0.57, 1.1, -0.61, -0.42, 0.67, 1.02, -1.56, -0.12, -0.37, 0.42, 0.36, -0.69, 0.86, -0.37, 1.06, 1.11, -0.31, -0.06)
seq2 <- c(1.2 ,-0.3 ,-1.03 ,0.05 ,0.95 ,0.84 ,0.55 ,1.46 ,0.3 ,1.05 ,-1.51 ,0.31 ,0.26 ,1.01 ,-1.73 ,0.79 ,-0.55 ,0.76 ,0.76 ,1.55 ,0.97)

lnorm <- function(m = 0, s = 1) {
  -sum(stats::dnorm(seq1, mean = m, sd = s, log = TRUE))
}

luni <- function(min = -1, max = 1) {
  -sum(stats::dunif(seq2, min = min, max = max, log = TRUE))
}

cnorm = stats4::mle(lnorm, method="L-BFGS-B", lower=c(0, 0))@coef
cuni = stats4::mle(luni, method="L-BFGS-B", lower=c(-1, 1))@coef

m_norm = unname(cnorm[1])
sd_norm = unname(cnorm[2])

m_uni = unname(cuni[1]) + unname(cuni[2])
sd_uni = std_dev(seq2)

cat("Sequence 1:\n")
print_intervals(seq1, 0.99, mnorm, sd_norm)

cat("\nSequence 2:\n")
print_intervals(seq2, 0.99, muni, sd_uni)