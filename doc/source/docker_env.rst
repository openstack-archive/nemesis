=================
Docker All In One
=================

Whilst Nemesis is in early development we have created a Docker All In One (AIO) image which contains a fully functional
self contained Nemesis environment to play with including:

* Ubuntu Base OS
* MySQL
* RabbitMQ
* Memcached
* Swift
* Keystone
* Nemesis API
* Nemesis Worker with ClamAV and EXIF plugins

*Warning: It is only recommended to run the Docker AIO image for dev / test purposes. If you wish to deploy Nemesis
properly to your environment please read the docs and deploy a suitable highly redundant configuration to avoid
dissapointment.*

To run the Docker AIO simply::
	
	docker run -it --privileged=true robputt796/nemesis-aio

Why privileged? This is the only way I could work out how to get mknod to work in a container to create a loop device for Swift.
If someone can let me know via a blueprint (https://blueprints.launchpad.net/python-nemesis) just how to enable this one capability
that would be awesome!

Once in the bash shell run the start script, source the openstack_user.rc file and generate a token using the OpenStack CLI,
once you have a token you can start using the local Nemesis API on port 9000::
	
	./start.sh
	source openstack_user.rc
	openstack token issue
	curl -H 'X-Auth-Token: $TOKEN' http://localhost:9000/v1/file

If you'd like to perform any administrative functions then you may source the openstack_admin.rc file for a user with the
administrative role::
	
	source openstack_admin.rc
