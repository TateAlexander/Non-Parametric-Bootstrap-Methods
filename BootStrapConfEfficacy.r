# How reliable is the Bootstrap confidence interval for variance (for exp[rate = 2])?
pop_var <- 0.25
alpha <- 0.05

est <- function(samples, n_iters){
  vars <- numeric(n_iters)
  
  for (i in 1:n_iters){
    resample <- sample(samples, length(samples), replace = TRUE)
    vars[i] <- var(resample)
  }
  quantile(vars, c(alpha/2, 1-alpha/2))
}

n_sims <- 200
test <- replicate(n_sims, expr = {
  s1 <- rexp(1000, rate = 2)
  ci <- est(s1, 1000)
  
  as.integer(pop_var > ci[1] & pop_var < ci[2])
})

# Compute the proportion of times the true variance is within the confidence interval
mean(test)
