sequence <- c(1.63, -2.47, 0.18, 1.14, -2.37, -0.94, 0.06, -1.05, -0.81, 0.03, -1.93, 0.41, -0.92,
              -0.16, -1.15, 0.56, 1.05, 0.41, -0.08, 1.23, -0.56, 0.67, 0.34, 1.05, -1.21, -0.31, 
              0.87, 2.2, -0.66, 0.74, -0.91, 2.72, 0.89, 0.6, 0.81, 2.36, 1.26, -0.92, -1.82, 0.09, 
              0.69, 0.47, -1.56, 0.2, -0.09, -1.28, 0.59, 0.4, -0.96, -0.01, 1.34, -0.26, -1.13, 
              -0.64, 0.73, -0.47, 0.93, -0.02, -0.92, -0.08, 0.26, -1.59, -0.52, 0.61, 1.34, 0.43, 
              0.02, 0.85, 0.23, 0.97, -0.66, 0.05, -0.16, -1.38, -0.82, -0.22, 1.3, 1.61, 0.23, 
              -2.55, 0.31, -2.02, 0.18, -0.79, -2.54, 0.97, -0.17, -2.15, -2.04, -0.48, 0.54, -0.27, 
              0.42, -1.7, 0.3, 0, 1.04, 0.85, 1.03, 0.4)

alpha <- 0.05

h = hist(sequence, breaks = 10, xlab = "Breaks")
c_test = chisq.test(h$counts)
if (c_test$p.value < alpha) {
  cat("Sample is normal distributed, p-value: ", c_test$p.value, "\n")
} else {
  cat("There are no reason to belive that sample is normal distributed, p-value: ", c_test$p.value, "\n")
}

ks_sample = unique(sequence)
ks_test = ks.test(ks_sample, 'pnorm', mean(sequence), sd(sequence), alternative = c("t"))

if (ks_test$p.value > alpha) {
  cat("Sample is normal distributed, p-value: ", ks_test$p.value, "\n")
} else {
  cat("There are no reason to belive that sample is normal distributed, p-value: ", ks_test$p.value, "\n")
}