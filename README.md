# openshift-applier

[![Project Status](http://opensource.box.com/badges/active.svg)](http://opensource.box.com/badges)

The openshift-applier is a service that continuously checks a git repository for new K8S objects and applies them with the oc client.
Based on the idea of the box/kube-applier, the openshift-cluster-applier runs as a Pod in your cluster and applies .yaml, .yml and .json files.
