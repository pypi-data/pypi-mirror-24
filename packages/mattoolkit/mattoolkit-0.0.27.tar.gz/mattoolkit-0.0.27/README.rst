Mattoolkit CLI
================================

Used to execute the queued VASP calculations. Needs to be installed on
all clients to run jobs from the Material Toolkit.



Handling Port Restrictions
==========================

.. code-block:: bash

   function ssh_tunnel()
   {
        if [[ $(ps aux | grep "[s]sh -D 8443") ]]; then
	     echo "SSH proxy already exists"
        else
             echo "SSH socks proxy created on port 8443"
	     ssh -D 8443 -f -C -q -N newton
        fi
   }

   function tunnel_if_no_http()
   {
        if [[ $(nc -vz google.com 80 -w 1 |& grep failed) ]]; then
	    ssh_tunnel

	    export http_proxy=socks5://localhost:8443/
	    export https_proxy=socks5://localhost:8443/
        fi
   }

   tunnel_if_no_http
