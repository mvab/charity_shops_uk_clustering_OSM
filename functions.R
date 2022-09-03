#' Replace outliers
#'
#' Replace outliers with NA. Outliers are defined as values that fall outside plus or minus
#' 1.5 * IQR.
#'
#' @return Numeric vector of same length.
#' @param x Numeric vector to replace.
#' @param na.rm Should NA values be replaced beforehand?
#'
#' @export
remove_outliers <- function(x, na.rm = TRUE, ...) {
  #qnt <- quantile(x, probs = c(.25, .75), na.rm = na.rm, ...)
  qnt <- quantile(x, probs = c(0.05, 0.95), na.rm = na.rm, ...)
  val <- 1.5 * IQR(x, na.rm = na.rm)
  y <- x
  y[x < (qnt[1] - val)] <- NA
  y[x > (qnt[2] + val)] <- NA
  y
}