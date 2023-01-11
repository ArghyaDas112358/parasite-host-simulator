import matplotlib.pyplot as mp
import numpy as np
import os
import numpy.linalg as la

train_data_path='./emotion_classification/train/'
test_data_path='./emotion_classification/test/'

def PCA(X,K):
    N,D = X.shape
    S_dash=np.cov(X)
    eigvals, eigvecs = la.eigh(S_dash)
    eigvecs=eigvecs[np.argsort(-1*eigvals)]
    eigvals=eigvals[np.argsort(-1*eigvals)]
    res_pca=1/np.sqrt(eigvals*N)*np.dot(X.T,eigvecs)
    return res_pca[:,:K]

def LDA(a,Y):
    X_c1=np.array([a[i] for i in range(len(X)) if Y[i]==0])
    X_c2=np.array([a[i] for i in range(len(X)) if Y[i]==1])
    m_1=np.mean(X_c1,axis=0)
    m_2=np.mean(X_c2,axis=0)
    S_b=np.dot(m_2-m_1,(m_2-m_1).T)

    cov1 = np.cov(X_c1.T)
    cov2 = np.cov(X_c2.T)
    S_w=cov1+cov2
    w = np.dot(la.inv(S_w),S_b)
    return w[:,0]

emotion_v2k = {0:"sad",1:"happy"}
emotion_k2v = {"sad":0,"happy":1}

ind = 1
Y_train=[]
for file in sorted(os.listdir(train_data_path)):
    for emotion in emotion_k2v:
        if emotion in file:
            Y_train.append(emotion_k2v[emotion])
    image = np.matrix(mp.imread(train_data_path+file))
    image=image.flatten('F')
    image=image-np.mean(image)
    if ind==1:
        X=np.array(image)
    else:
        X=np.concatenate((X,np.array(image)))
    ind = ind+1

ind = 1
Y_test=[]
for file in sorted(os.listdir(test_data_path)):
    for emotion in emotion_k2v:
        if emotion in file:
            Y_test.append(emotion_k2v[emotion])
    image = np.matrix(mp.imread(test_data_path+file))
    image=image.flatten('F')
    image=image-np.mean(image)
    if ind==1:
        test=np.array(image)
    else:
        test=np.concatenate((test,np.array(image)))
    ind = ind+1

Y_train=np.array(Y_train)
Y_test=np.array(Y_test)

tmp_Y_train = Y_train
tmp_Y_test = Y_test
tmp_X = X
tmp_test = test

K=19
res_pca=PCA(X,K)
trained=np.dot(X,res_pca)

print('Trained Data')
res_lda=LDA(trained,Y_train)
plt = np.dot(res_lda, trained.T)
threshold=(np.max(plt)+np.min(plt))/2
x=np.array(range(1,len(plt)+1))
mp.plot(x,plt,'bo')
mp.plot(x,x*0+threshold)
mp.show()

crr1=[]
for i in range(len(plt)):
    if plt[i]<threshold:
        crr1.append(1)
    else:
        crr1.append(0)
crr1=np.array(crr1)

acc1=sum(crr1==Y_train)/len(crr1)*100
print("Accuracy = %.2f" % acc1)

print()
print('Test Data')
test = np.dot(test,res_pca)
plt = np.dot(res_lda, test.T)
x=np.array(range(1,len(plt)+1))
mp.plot(x,plt,'ro')
mp.plot(x,x*0+threshold)
mp.show()

crr2=[]
for i in range(len(plt)):
    if plt[i]<threshold:
        crr2.append(1)
    else:
        crr2.append(0)
crr=np.array(crr2)

acc2=sum(crr==Y_test)/len(crr2)*100
print("Accuracy = %.2f" % acc2)


def Accuracy(K=3):
    print("---------------------------------------")
    print("Choosing K = ",K)
    res_pca=PCA(X,K)
    trained=np.dot(X,res_pca)

    res_lda=LDA(trained,Y_train)
    plt = np.dot(res_lda, trained.T)
    threshold=(np.max(plt)+np.min(plt))/2
    x=np.array(range(1,len(plt)+1))

    crr1=[]
    for i in range(len(plt)):
        if plt[i]<threshold:
            crr1.append(1)
        else:
            crr1.append(0)
    crr1=np.array(crr1)

    acc1=sum(crr1==Y_train)/len(crr1)*100
    print("Trained Accuracy = ",acc1,"%")

    test = np.dot(tmp_test,res_pca)
    plt = np.dot(res_lda, test.T)
    x=np.array(range(1,len(plt)+1))

    crr2=[]
    for i in range(len(plt)):
        if plt[i]<threshold:
            crr2.append(1)
        else:
            crr2.append(0)
    crr=np.array(crr2)

    acc2=sum(crr==tmp_Y_test)/len(crr2)*100
    print("Trained Accuracy = ",acc2,"%")

for i in range(2,20):
    Accuracy(i)
print("---------------------------------------")
print("Thus we see that the maximum accuracy in the test daa is obtained for K = 19")