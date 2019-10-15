@echo off
REM Used for quickly generating new models
REM Change the values below before executing
REM Because i'm tired of doing this through the
REM command line

REM Note: This does not download or process the training
REM data. Please download the training data and run the
REM autoscale.py script first
REM @echo off
REM Values to change************
SET /A inputWidth=480
SET /A inputHeight=270
SET /A epochs=1000
SET trainSrc=./images_scaled/training
SET modelName=tmodel
SET distortions=--random_crop 7 --random_scale 5 --random_brightness 10
SET srcModel=https://tfhub.dev/google/imagenet/mobilenet_v1_100_224/feature_vector/3

REM Don't change below**********

REM Check if powershell or CMD for multiline command

python retrain.py ^
    --image_dir %trainSrc% ^
    %distortions% ^
    --how_many_training_steps %epochs% ^
    --tfhub_module %srcModel% ^
    --output_graph ./%modelName%/output_graph.pb ^
    --intermediate_output_graphs_dir ./%modelName%/intermediate/graph/ ^
    --output_labels ./%modelName%/output_labels.txt ^
    --summaries_dir ./%modelName%/retrain_logs ^
    --bottleneck_dir ./%modelName%/bottleneck ^
    --saved_model_dir ./%modelName% ^
    --checkpoint_path ./%modelName%

REM python retrain.py --image_dir ./images_scaled/images/training