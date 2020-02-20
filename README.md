# openshift-applier

[![Project Status](http://opensource.box.com/badges/active.svg)](http://opensource.box.com/badges)

## Summary
The openshift-applier is a service that continuously checks a git repository for new K8S objects and applies them with the oc client. The service runs as a Pod in your cluster and applies .yaml, .yml and .json files.

## Requirements
- `Docker (17.05+)`
- `Python (>2.7)`
- `OpenShift cluster`

## Templates
[Templates](https://github.com/JonasGovaerts/openshift-applier/tree/development/templates) are available to deploy all needed objects to use the openshift-applier on namespace and on cluster level.
In these templates, following variables are used: 
* **`REPOSITORY`**
* **`USERNAME`** (optional)
* **`PASSWORD`** (optional)
* **`BRANCH`** (default points to development)
* **`TIMER`** (default to 60 seconds)

### Variables
**`REPOSITORY`**

**`USERNAME`**

**`PASSWORD`**

**`BRANCH`**

**`TIMER`**

## Copyright and License
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

