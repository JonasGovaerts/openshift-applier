# openshift-applier

[![Project Status](http://opensource.box.com/badges/active.svg)](http://opensource.box.com/badges)

openshift-applier is a service that enables continuous deployment of Kubernetes objects by applying declarative configuration files from a Git repository to an OpenShift cluster.

openshift-applier runs as a Pod in your cluster and watches the [Git repo](#mounting-the-git-repository) to ensure that the cluster objects are up-to-date with their associated spec files (JSON or YAML) in the repo.

At a [specified interval](#run-interval), openshift-applier performs a "full run", issuing the oc apply  command for all JSON, YML and YAML files within the repo.

When a new commit to the repo occurs, openshift-applier performs a "quick run", issuing apply commands only for files that have changed since the last run.

Quick runs and full runs are handled separately and concurrently.

openshift-applier serves a [status page](#status-ui) and provides [metrics](#metrics) for monitoring.
