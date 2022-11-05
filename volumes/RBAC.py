
 
openssl genrsa -out emp.key 2048 

 
openssl req -new -key emp.key -out emp.csr -subj "/CN=emp/O=dev" 

 
openssl x509 -req -in emp.csr -CA CA_FOLDER/ca.crt -CAkey CA_FOLDER/ca.key -CAcreateserial -out emp.crt -days 500 
Note: Change CA_FOLDER value by either ~/.minikube/. or /etc/kubernetes/pki/. based on your CA files location 

 
kubectl create namespace dev 

 
kubectl config set-context dev-ctx --cluster=minikube --namespace=dev --user=emp 

 
kubectl config set-credentials emp --client-certificate=./emp.crt  --client-key=./emp.key 
Run cat ~/.kube/config. You should see above added information in that config file. 

 
kind: Role 
apiVersion: rbac.authorization.k8s.io/v1beta1 
metadata: 
  namespace: dev 
  name: emp-role 
rules: 
- apiGroups: ["", "extensions", "apps"] 
  resources: ["deployments",  "pods"] 
  verbs: ["get", "list"] 
 


 
kind: RoleBinding 
apiVersion: rbac.authorization.k8s.io/v1beta1 
metadata: 
  name: emp-bind 
  namespace: dev 
subjects: 
- kind: User 
  name: emp 
  apiGroup: "" 
roleRef: 
  kind: Role 
  name: emp-role 
  apiGroup: "" 
 

 
Testing

kubectl --context=employee-context get pods
kubectl --context=employee-context run --image=nginx

