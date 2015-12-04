library(ppls)

get_disp <- function(vec, step, conf_level = 0.99) {
  left_border <- min(vec)
  right_border <- max(vec)
  answer = c()
  norm = c()
  
  for (i in seq(from = left_border, to = right_border - step, by = step)) {
    answer = c(answer, length(vec[vec >= i & vec < i + step]))
    norm = c(norm, pnorm(i + step) - pnorm(i))
  }
  
  answer <- normalize.vector(answer)
  answer <- answer / sum(answer)
  
  print(answer)
  
  stat <- sum((answer - norm) ** 2 / norm)
  s_val <- qchisq((1 + conf_level) / 2, df = length(answer) - 1)
  
  c(stat, s_val)
}

print_hypotesis <- function(seq, conf_level)
{
  m = mean(seq)
  std_dev = sd(seq)
  d_f = length(seq) - 1
  
  left_disp = d_f * std_dev ** 2 / qchisq((1 + conf_level) / 2, df = d_f)
  right_disp = d_f * std_dev ** 2 / qchisq((1 - conf_level) / 2, df = d_f)
  res = t.test(seq, conf.level = conf_level)

  cat("Mean: ", m, "; interval: (", res$conf[1], " - ", res$conf[2], ")\n")
  cat("Dispersion: ", std_dev ** 2, "; interval: (", left_disp, " - ", right_disp, ")\n")
}

sequence <- c(1.63, -2.47, 0.18, 1.14, -2.37, -0.94, 0.06, -1.05, -0.81, 0.03, -1.93, 0.41, -0.92,
              -0.16, -1.15, 0.56, 1.05, 0.41, -0.08, 1.23, -0.56, 0.67, 0.34, 1.05, -1.21, -0.31, 
              0.87, 2.2, -0.66, 0.74, -0.91, 2.72, 0.89, 0.6, 0.81, 2.36, 1.26, -0.92, -1.82, 0.09, 
              0.69, 0.47, -1.56, 0.2, -0.09, -1.28, 0.59, 0.4, -0.96, -0.01, 1.34, -0.26, -1.13, 
              -0.64, 0.73, -0.47, 0.93, -0.02, -0.92, -0.08, 0.26, -1.59, -0.52, 0.61, 1.34, 0.43, 
              0.02, 0.85, 0.23, 0.97, -0.66, 0.05, -0.16, -1.38, -0.82, -0.22, 1.3, 1.61, 0.23, 
              -2.55, 0.31, -2.02, 0.18, -0.79, -2.54, 0.97, -0.17, -2.15, -2.04, -0.48, 0.54, -0.27, 
              0.42, -1.7, 0.3, 0, 1.04, 0.85, 1.03, 0.4)

s2 <- runif(1000, -3, 3)

get_disp(s2, 0.4)


