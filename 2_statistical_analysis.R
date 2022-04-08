# SETUP VARIABLES: 
# Setup r to read current directory
library(rstudioapi)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# Set seed
set.seed(2022)

#===============================================================================
# MIXED LINEAR REGRESSION ANALYSIS:

# Prepare Data
windowedData = read.csv("processed_data/dataset1.csv")
library(caTools) 
splitWindow =sample.split(windowedData,SplitRatio = 0.8) 
trainWindow = subset(windowedData,splitWindow == TRUE) 
testWindow = subset(windowedData,splitWindow == FALSE) 
nrow(trainWindow) # Print sizes
nrow(testWindow)

# Train Model 
library(lme4)
library(lmerTest)
library(jtools)
print("ENGAGEMENT:")
mixedModel <- lmer(engagement ~ noteEdit 
                                + paramChange 
                                + building 
                                + playback 
                                + navigate
                                + (1 | ID), data=trainWindow)
#summary(mixedModel)
summ(mixedModel)
#ranova(mixedModel)

# Test Accuracy
library(caret)
mixedPredict <- predict(mixedModel, testWindow) 
results = data.frame(R2 = R2(mixedPredict, testWindow$engagement),
            RMSE = RMSE(mixedPredict, testWindow$engagement),
            MAE = MAE(mixedPredict, testWindow$engagement))
results

print("FOCUSED ATTENTION:")
mixedModel <- lmer(focusedAttention ~ noteEdit 
                   + paramChange 
                   + building 
                   + playback 
                   + navigate
                   + (1 | ID)
                   + (1 | musicLessonConfidence), data=trainWindow)
summ(mixedModel)
mixedPredict <- predict(mixedModel, testWindow) 
results = data.frame(R2 = R2(mixedPredict, testWindow$engagement),
                     RMSE = RMSE(mixedPredict, testWindow$engagement),
                     MAE = MAE(mixedPredict, testWindow$engagement))
results

print("CLEAR GOALS:")
mixedModel <- lmer(clearGoals ~ noteEdit 
                   + paramChange 
                   + building 
                   + playback 
                   + navigate
                   + (1 | ID), data=trainWindow)
summ(mixedModel)
mixedPredict <- predict(mixedModel, testWindow) 
results = data.frame(R2 = R2(mixedPredict, testWindow$engagement),
                     RMSE = RMSE(mixedPredict, testWindow$engagement),
                     MAE = MAE(mixedPredict, testWindow$engagement))
results

print("CLEAR CUT FEEDBACK:")
mixedModel <- lmer(clearCutFeedback ~ noteEdit 
                   + paramChange 
                   + building 
                   + playback 
                   + navigate
                   + (1 | ID), data=trainWindow)
summ(mixedModel)
mixedPredict <- predict(mixedModel, testWindow) 
results = data.frame(R2 = R2(mixedPredict, testWindow$engagement),
                     RMSE = RMSE(mixedPredict, testWindow$engagement),
                     MAE = MAE(mixedPredict, testWindow$engagement))
results

print("PLEASURE:")
mixedModel <- lmer(pleasure ~ noteEdit 
                   + paramChange 
                   + building 
                   + playback 
                   + navigate
                   + (1 | ID), data=trainWindow)
summ(mixedModel)
mixedPredict <- predict(mixedModel, testWindow) 
results = data.frame(R2 = R2(mixedPredict, testWindow$engagement),
                     RMSE = RMSE(mixedPredict, testWindow$engagement),
                     MAE = MAE(mixedPredict, testWindow$engagement))
results

#===============================================================================

# DECISION TREE:
library(rpart)
library(rpart.plot)

# Create the overfit tree using all data
df <- read.csv("processed_data/dataset1b.csv")
fulltree = rpart(formula = engagement ~ noteEdit + paramChange + building + playback + navigate, 
              data=df)
rpart.plot(fulltree, type=1, digits=2, yesno=2, extra=100, fallen.leaves=TRUE, box.palette="GnRd")

# Test-Train split for window data
library(caTools) 
split =sample.split(df,SplitRatio = 0.8) 
train = subset(df,split == TRUE) 
test = subset(df,split == FALSE) 

nrow(train) # Print sizes
nrow(test)

# Find the best tree based on the leave-one-out cross validation procedure
library(caret)
control <- trainControl(method = "LOOCV")
model <- train(engagement ~ noteEdit + paramChange + building + playback + navigate, 
               data = train,
               method = "rpart",
               trControl = control)
model 

prunedtree <- prune(fulltree, cp = 0.03515625) #<-- obtain cp from printout of model 
rpart.plot(prunedtree, type=1, digits=2, yesno=2, extra=100, fallen.leaves=TRUE, box.palette="GnRd") 

# Print ML metrics 
tPredict <- predict(prunedtree, test, type="class") 
confMat = table(test$engagement,tPredict)

TP <- confMat[1]
FN <- confMat[3]
FP <- confMat[2]
TN <- confMat[4]

accuracy <- sum(diag(confMat))/sum(confMat)
accuracy

precision <- TP/(TP+FP)
precision

recall = TP/(TP+FN)
recall 

F1 = (2*(recall*precision)) / (recall+precision)
F1
