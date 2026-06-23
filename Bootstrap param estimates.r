samples <- rexp(100, rate = 1)
samples


boot_var <- function(samples, r){
  vars <- c()
  for (i in 1:r){
    resample <- sample(samples, length(samples), replace = TRUE)
    vars <- c(vars, var(resample))
  }
  vars
}
boot_vars <- boot_var(samples, 10000)
hist(boot_vars)

conf_95 <- quantile(boot_vars, probs = c(0.025, 0.975))
conf_95


bias_var <- mean(boot_vars) - var(samples)
bias_var

# Basic Bootstrap confidence interval

t_var <- var(samples)

basic_var_ci <- c(
  2 * t_var - quantile(boot_vars, 0.975),
  2 * t_var - quantile(boot_vars, 0.025)
)

basic_var_ci


# Two population mean ratio example

pop1 <- rnorm(n = 200, mean = 1000, sd = 25)
pop2 <- rnorm(n = 200, mean = 750, sd = 15)

pop_ratio <- mean(pop1) / mean(pop2)

boot_ratio <- function(sample1, sample2, r){
  boot_estimates <- c()
  for (i in 1:r){
    resample_1 <- sample(sample1, length(sample1), replace = TRUE)
    resample_2 <- sample(sample2, length(sample2), replace = TRUE)
    
    estimate <- mean(resample_1) / mean(resample_2)
    boot_estimates <- c(boot_estimates, estimate)
  }
  boot_estimates
}

est <- boot_ratio(pop1, pop2, 10000)
hist(est)

boot_ratio_bias <- mean(est) - pop_ratio
boot_ratio_bias

boot_95conf <- quantile(est, probs = c(0.025, 0.975))
boot_95conf
