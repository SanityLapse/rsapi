#!/usr/bin/python -tt

# Copyright 2013 Chris Hughes (christopher.hughes@rackspace.com)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyrax
import argparse
import os
import time
import argparse

def main():
          
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flavor', default=2, help='Flavor for new cloud servers')
    parser.add_argument('-i', '--image', default='e4dbdba7-b2a4-4ee5-8e8f-4595b6d694ce', help='Flavor for new cloud servers')
    parser.add_argument('-b', '--basename', default='New', help='Base name for the servers. For example \'Web\' would produce servers of the names Web1, Web2, etc')
    parser.add_argument('-q', '--quantity', default=3, help='Quantity of servers you want to spin up. The default is 3.')

    args = parser.parse_args()
    
    pyrax.set_credential_file(os.path.join(os.path.expanduser("~"), "rs-creds"))
    
    cs = pyrax.cloudservers
    
    n = 0
    new_servers = []
    while n <= args.quantity - 1 :
        print "Spinning up server " + args.basename + str(n + 1)
        new_servers.append(cs.servers.create(args.basename + str(n + 1), args.image, args.flavor))
        p = 0
        while p < 100:
            p = cs.servers.get(new_servers[n].id).progress
            time.sleep(10)
            print "Progress: " + str(p) + "%"
        n += 1
        
    print "All server builds complete:"
    print ""
    for srv in new_servers:
        print "Name: " + srv.name
        print "ID: ", srv.id
        print "Admin password: ", srv.adminPass
        print ""
   
if __name__ == '__main__':
    main()
    