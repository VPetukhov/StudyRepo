m_sign <- function(x) {
  y = c()
  for (v in x)
  {
    if (v >= 0)
    {
      y = c(y, 1)
    }
    else
    {
      y = c(y, -1)
    }
  }
  y
}

get_sign_coeff <-function(x, y)
{
  sum(m_sign(x - median(x)) * m_sign(y - median(y))) / length(x)
}

get_coeffs <- function(x, y)
{
  pearson = cor(x, y, method = "pearson")
  quartile = get_sign_coeff(x, y)
  kendall = cor(x, y, method = "kendall")
  spearman = cor(x, y, method = "spearman")
  
  cat("Pearson: ", pearson, "\n")
  cat("Quartile: ", quartile, "\n")
  cat("Spearman: ", spearman, "\n")
  cat("Kendall: ", kendall, "\n")
  
  quartile = sin(pi * quartile / 2)
  spearman = 2 * sin(pi * spearman / 6)
  kendall = sin(pi * kendall / 2)
  
  print("Modified:\n")
  cat("Quartile: ", quartile, "\n")
  cat("Spearman: ", spearman, "\n")
  cat("Kendall: ", kendall, "\n")
}


x0 <- MASS::mvrnorm(40, c(0, 0), matrix(c(1, 0, 0, 1), 2, 2))
x5 <- MASS::mvrnorm(40, c(0, 0), matrix(c(1, 0.5, 0.5, 1), 2, 2))
x9 <- MASS::mvrnorm(40, c(0, 0), matrix(c(1, 0.9, 0.9, 1), 2, 2))

print(x9)
get_coeffs(x0[,1], x0[,2])
get_coeffs(x5[,1], x5[,2])
get_coeffs(x9[,1], x9[,2])
