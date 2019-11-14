- create a lab device manager that:
  - allows users to create, update, and delete lab devices
  - maps a production device to a lab device
  - maps production device interfaces to lab device interfaces
  - makes calls to EVE-NG (https://www.eve-ng.net/) to pull access details about lab devices 
  - consumes a production config from an associated production device
    - formats the config for the lab
    - installs the config onto the lab device

- create a production device manager that:
  - periodically pulls the most recent production config from production devices

- create a secure secrets database that:
  - allows users to create, update, and delete secrets securely

- technologies:
  - django
  - hier_config
  - netmiko
  - rabbitmq
  - celery
