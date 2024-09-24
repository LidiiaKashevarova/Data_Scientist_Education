#Loud packages and library 
install.packages("car")  
library(car) 
library("readxl")
library(Metrics)
library(leaps)  

#load and check database 
file_path <- "C:/Users/lidii/Documents/ec/R/R_kunskapskontroll_L.Kashevarova/data_car.xlsx"

data_car <- read_excel(file_path)
View(data_car)
dim(data_car)
head(data_car)
summary(data_car)
sum(is.na(data_car))


#Dividing the base into training data, validation data and test data_________ 
spec = c(train = .6, validate = .2, test = .2) 

set.seed(123) 
g = sample(cut(  
  seq(nrow(data_car)), 
  nrow(data_car)*cumsum(c(0,spec)),
  labels = names(spec)
))

res = split(data_car, g)

data_car_train <- res$train
data_car_val <- res$validate
data_car_test <- res$test


#Training af model 1_________________________________________________
lm_1 <- lm(pris_kr ~ ., data = data_car_train)
summary(lm_1)

par(mfrow = c(1, 4))
plot(lm_1)

vif(lm_1)


#Training af model 2_________________________________________________
lm_2 <- lm(pris_kr~.- Horsepower_Hp, data = data_car_train)    
summary(lm_2)

par(mfrow = c(1, 4))
plot(lm_2)

vif(lm_2)



# Predictions on validation data:______________________________

#Model 1 
val_pred_m1 <- predict(lm_1, newdata = data_car_val)

#Model 2 
val_pred_m2 <- predict(lm_2, newdata = data_car_val)


#Summary results for 2 models with validation data
results <- data.frame(
  Model = c("Model 1", "Model 2"),
  RMSE_val_data = c(rmse(data_car_val$pris_kr, val_pred_m1), 
                    rmse(data_car_val$pris_kr, val_pred_m2)),
  
  Adj_R_squared = c(summary(lm_1)$adj.r.squared,
                    summary(lm_2)$adj.r.squared),
  
  BIC = c(BIC(lm_1), BIC(lm_2))
)

results

#Predictions on testing data_______________________________

test_pred_m1 <- predict(lm_1, newdata = data_car_test)

RMSE_test <- rmse(data_car_test$pris_kr, test_pred_m1)
print(RMSE_test)

#R^2 test data 

a <- data_car_test$pris_kr - test_pred_m1
RSS <- sum(a^2)
TSS <- sum((data_car_test$pris_kr - mean(data_car_test$pris_kr))^2)
rsquared <- 1 - RSS / TSS

print(rsquared)



# New data that we want to predict_________________________________
new_data <- data.frame(
  Model_year = c(2018, 2020,2023),
  mil = c(12000, 7000, 3000),
  Fuel_Hybrid_0_Bensin_1_Diesel_2 = c(2, 2, 0), 
  Gearbox_Automat_0_Manuell_1 = c(0, 0, 0),
  Horsepower_Hp = c(150, 150, 400)
) 

# Create CI & PI for predictions for new data
confidence_intervals <- predict(lm_1, newdata = new_data, interval = "confidence", level = 0.95)
prediction_intervals <- predict(lm_1, newdata = new_data, interval = "prediction", level = 0.95)

confidence_intervals
prediction_intervals



#Test data with other car`s marks__________________________________________

file_other_mod <- "C:/Users/lidii/Documents/ec/R/R_kunskapskontroll_L.Kashevarova/test_data_1.xlsx"
test_data <- read_excel(file_other_mod)

View(test_data)
dim(test_data)
head(test_data)
summary(test_data)

predictions_other_mark <- predict(lm_1, newdata = test_data)

RMSE_other_mark <- rmse(test_data$pris_kr, predictions_other_mark)

print(RMSE_other_mark)

#R^2 data with other car`s marks

a <- test_data$pris_kr - predictions_other_mark
RSS <- sum(a^2)
TSS <- sum((test_data$pris_kr - mean(test_data$pris_kr))^2)
rsquared <- 1 - RSS / TSS
print(rsquared)




