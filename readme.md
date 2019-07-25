### 运行流程

#### 离线训练
##### 根据conda.yaml初始化conda环境（python版本，依赖库等）
##### 调用MLproject中指定的train命令执行自定义的train方法，需自行保存模型

###### 示例

**train data1 as PythonAlg.`/tmp/model` where
pythonScriptPath="/home/user/mlsql_example"
and fitParam.0.featureCol="features"
and fitParam.0.labelCol="label"
and fitParam.0.moduleName="sklearn.svm"
and fitParam.0.className="SVC";**

#### 离线预测 
##### 调用MLproject中指定的batch_predict命令执行自定义方法进行预测

###### 示例

**predict data1 as PythonAlg.`/tmp/model` as output;**

#### 注册模型
##### 调用engine接口将模型注册为函数供调用，函数的执行逻辑即MLproject中指定的api_predict命令

###### 示例

**Api endpoint: http://127.0.0.1:9003/run/script**

**sql=register PythonAlg.`/home/mlsql/user/tmp/model` as sk_predict;**

#### 调用接口
##### 调用engine提供的接口进行预测

###### 示例

**Api endpoint: http://127.0.0.1:9003/model/predict**

**sql=select sk_predict(vec_dense(features)) as p1
&data=[ {"features": [4.7,3.2,1.3,0.2]}]
&dataType=row**

#### 问题记录

1. conda初始化失败的情况，在spark日志中难以发现具体原因，可以在服务器上执行**conda -n test -f conda.yaml**查看输出；
2. 训练完成后模型的实际保存路径，为用户输入的路径加上**/home/mlsql/user**前缀（user为登陆到console界面的用户），
在注册模型时，应使用完整路径；