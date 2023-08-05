#!/bin/env python
__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

import logging
import urllib

from vc3infoservice.core import InfoEntity
   
class User(InfoEntity):
    '''
    Represents a VC3 instance user account.
    As policy, name, email, and institution must be set.  

    JSON representation:
    {
        "user" : {
            "johnrhover": {
                "name"  : "johnrhover",
                "first" : "John",
                "last"  : "Hover",
                "email" : "jhover@bnl.gov",
                "institution" : "Brookhaven National Laboratory",
            },
        }
    }
    '''
    infoattributes = ['name',
                     'state',
                     'acl',
                     'first',
                     'last',
                     'email',
                     'institution',
                     'identity_id'] 
    infokey = 'user'
    validvalues = {}
    
    def __init__(self,
                   name,
                   state,
                   acl,
                   first,
                   last,
                   email,
                   institution,
                   identity_id=None):
        '''
        Defines a new User object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 username of this user
        :param str first: User's first name
        :param str last: User's last name
        :param str email: User's email address
        :param str institution: User's intitutional affiliation or employer
        :return: User:  A valid User object      
        :rtype: User
        '''
        self.log = logging.getLogger()
        self.state = state
        self.acl = acl
        self.name = name
        self.first = first
        self.last = last
        self.email = email
        self.institution = institution
        self.identity_id = identity_id
        self.log.debug("User object created: %s" % self)
        self.allocations = []

    def addAllocation(self, allocation):
        '''
            Adds provided allocation (string label) to this allocation.
        '''
        self.log.debug("Adding allocation %s to project" % allocation)
        if allocation not in self.allocations:
            self.allocations.append(allocation)
        self.log.debug("Allocations now %s" % self.allocations)
        

    def removeAllocation(self, allocation):
        '''
            Removes provided allocation (string label) to this project.
        '''
        self.log.debug("Removing allocation %s to project" % allocation)
        if allocation not in self.allocations:
            self.log.debug("Allocation %s did not belong to project")
        else:
            self.allocations.remove(allocation)
            self.log.debug("Allocations now %s" % self.allocations)


class Project(InfoEntity):
    '''
    Represents a VC3 Project.
    '''
    infokey = 'project'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'members', 
                     'allocations',
                     'blueprints']
    validvalues = {}
    
    
    def __init__(self, 
                   name,
                   state,
                   acl,
                   owner,
                   members,   # list
                   allocations=None,  # list of names 
                   blueprints=None):  # list of names
        '''
        Defines a new Project object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this project
        :param str owner: VC3 username of project owner. 
        :param str members: List of vc3 usernames
        :param str allocations: List of allocation names. 
        :param str blueprints:  List blueprint names. 
        :return: Project:  A valid Project objext. 
        :rtype: Project
        '''  
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner
        self.members = []
        for m in members:
            if m not in self.members:
                self.members.append(m)
        #self.members.append(owner)
        #if members is not None:
        #    for m in members:
        #        if m not in self.members:
        #            self.members.append(m)
        self.allocations = allocations
        self.blueprints = blueprints
        self.log.debug("Project object created: %s" % self)

    def addUser(self, user):
        '''
            Adds provided user (string label) to this project.
        '''
        self.log.debug("Adding user %s to project" % user)
        if user not in self.members:
            self.members.append(user)
        self.log.debug("Members now %s" % self.members)
        

    def removeUser(self, user):
        '''
            Removes provided user (string label) to this project.
        '''
        self.log.debug("Removing user %s to project" % user)
        if user not in self.members:
            self.log.debug("User %s did not belong to project")
        else:
            self.members.remove(user)
            self.log.debug("Members now %s" % self.members)

class Resource(InfoEntity):
    '''
    Represents a VC3 target resource. 
    
    "resource" : {
            "uchicago_rcc": {
                "resourcetype" : "remote-batch",  # grid remote-batch local-batch cloud
                "accessmode" : "MFA" # ssh, gsissh, 
                "submithost" : <hostname>,
                "submitport" : <port>,
                "type": "<batch-type>",
                "version": "14.11.11",
                },
            }
    
    intrinsic time limits/preemption flag to distinguish platforms we could run static components on. 
    network access is also critical for this.    
    '''
    infokey = 'resource'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'accesstype', 
                     'accessmethod',
                     'accessflavor',
                     'accesshost',
                     'accessport',
                     'gridresource',
                     'mfa'
                     ]
    validvalues = {}
    
    def __init__(self,
                 name,
                 state,
                 acl,
                 owner,
                 accesstype,   # grid, batch, cloud
                 accessmethod, # ssh, gsissh
                 accessflavor, # condor-ce, slurm, sge, ec2, nova, gce
                 accesshost,   # hostname
                 accessport,   # port
                 gridresource, # http://cldext02.usatlas.bnl.gov:8773/services/Cloud , HTCondor CE hostname[:port]              
                 mfa = False,
                 ):
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner
        
        # Entity-specific attriutes
        self.accesstype = accesstype
        self.accessmethod = accessmethod
        self.accessflavor = accessflavor
        self.accesshost = accesshost
        self.accessport = accessport
        self.gridresource = gridresource
        self.mfa = mfa
        self.log.debug("Resource object created: %s" % self)


class Allocation(InfoEntity):
    '''
    Represents the access granted a VC3 User and a VC3 target Resource.
    Defined by (resource, vc3user, unix_account) triple.   
    
    May or may not contain sub-Allocations.
    
    (Top-level) Allocation names are in the form <vc3username>.<vc3resourcename>.
    Sub-allocation names are in the form <vc3username>.<vc3resourcename>.<suballocationlabel>
            
    "johnrhover.sdcc-ic." : {
        "acl" : "rw:vc3adminjhover, r:vc3jhover",
        "username": "jhover",
            "security-token" : { 
            "type" : "ssh-keypair",
            "ssh-type" : "ssh-rsa",
            "ssh-pubkey" : "AAAAB3NzaC1...",
            "ssh-privkey" : "XXXXXXXXXXXX...",
            },    
        },
        "johnrhover.amazon-ec2" : {
            "user" : "johnrhover",
            "resource" : "amazon-ec2"
            "acl" : "rw:vc3adminjhover, r:vc3jhover",
            "accountname" : "racf-cloud@rcf.rhic.bnl.gov",
            "security-token" :  {
                "type" : "cloud-tokens",
                "accesskey" : "AAAAB3NzaC1...",
                "privatekey" : "XXXXXXXXXXXX...",
                }
            }
        },
        "johnrhover.bnl-cluster1" : {
            "username": "jhover",
            "security-token" : {
                "type" : "ssh-keypair",
                "ssh-type" : "ssh-rsa",
                "ssh-pubkey" : "AAAAB3NzaC1...",
                "ssh-privkey" : "XXXXXXXXXXXX...",
                }
            }
        }
    '''
    infokey = 'allocation'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'resource',
                     'type',
                     'accountname',
                     'quantity',
                     'units',
                     'sectype',     # ssh-rsa, ssh-dsa, pki, x509
                     'pubtoken',    # ssh pubkey, cloud access key
                     'privtoken',   # ssh privkey, cloud secret key, VOMS proxy
                    ]   
    validvalues = {}
    
    
    def __init__(self, 
                 name, 
                 state, 
                 acl, 
                 owner, 
                 resource, 
                 accountname, 
                 type='unlimited', 
                 quantity=None, 
                 units=None,
                 sectype=None,
                 pubtoken=None,
                 privtoken=None, 
                  ):
        '''
        :param str owner:         vc3username of owner of allocation
        :param str resource:      vc3 resource name 
        :param str type:          what sort of allocation (unlimited, limited, quota)
                
        '''
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner
        self.resource = resource
        self.accountname = accountname     # unix username, or cloud tenant, 
        self.type = type           # quota | unlimited | limited 
        self.quantity = quantity   # 
        self.units = units         #
        self.sectype = sectype
        self.pubtoken = pubtoken
        self.privtoken = privtoken


class Policy(InfoEntity):
    '''
    Describes the desired resource utilization policy when a Request 
    includes multiple Allocations. 
    
    '''
    infokey = 'policy'
    infoattributes = ['name',
                     'state',
                     'owner',
                     'acl',
                      'pluginname'
                      ]
    validvalues = {}
    
    
    def __init__(self, name, state, owner, acl, pluginname):
        ''' 
        "static-balanced" : {
                "pluginname" : "StaticBalanced",
            },
 
        "weighted-balanced" : {
                "pluginname" : "WeightedBalanced",
                "weightmap" : "sdcc-ic.johnrhover,.80,bnl-cluster1.johnrhover,.20"
            },
         
        "ordered-fill" : {
                "pluginname" : "OrderedFill",
                "fillorder: "sdcc-ic.johnrhover, bnl-cluster1.johnrhover,amazon-ec2.johnrhover" 
        }
        
        '''
        self.name = name
        self.owner = owner
        self.acl = acl
        self.pluginname = pluginname
        
        

class Cluster(InfoEntity):
    '''
    Represents a supported VC3 middleware cluster application, node layout, and all relevant 
    configuration and dependencies to instantiate it. It is focussed on building the virtual 
    *cluster* not the task/job Environment needed to run a particular user's domain application. 
    
    Cluster descriptions should be generic and shareable across Users/Projects. 
    
    e.g. 
         vc3-factory-dynamic
         htcondor-managed-cm-schedd
         htcondor-managed-cm-ext-schedd
         workqueue-managed-catalog
         workqueue-ext-catalog
         ?
        }
    '''
    infokey = 'cluster'
    infoattributes = [ 'name',
                        'state',
                        'owner',
                        'acl',
                        'nodesets',
                      ]
    validvalues = {}


    def __init__(self, name, state, owner, acl, nodesets ):
        '''

        '''
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.owner = owner
        self.acl = acl
        self.nodesets = [] # ordered list of nodeset labels


    def addNodeset(self, nodesetname ):
        if nodesetname not in self.nodesets:
            self.nodesets.append(nodesetname)

    def removeNodeset(self, nodesetname):
        if nodesetname in self.nodesets:
            self.nodesets.remove(nodesetname)


class Nodeset(InfoEntity):
    '''
    Represents a set of equivalently provisioned nodes that are part of a Cluster definition. 
    
        "nodes" : {
            "headnode1" : {
                "node_number" : "1",
                "node_memory_mb" : "4000",
                "node_cores_minimum" : "4",
                "node_storage_minimum_mb" : "50000",
                "app_type" : "htcondor",
                "app_role" : "head-node",
                "app_port" : "9618"
                "app_password" : "XXXXXXX",
            },
            "workers1" : {
                "app_depends" : "headnode1",
                "node_number" : "10",
                "node_cores_minimum" : "8",
                "node_memory_mb" : "4000",
                "node_storage_minimum_mb" : "20000",
                "app_type" : "htcondor",
                "app_role" : "execute",
                "app_host" : "${HEADNODE1}.hostname",
                "app_port" : "9618"
                "app_password" : "XXXXXXX",
            },
        }
    '''
    infokey = 'nodes'
    infoattributes = ['name',
                     'state',
                     'owner',
                     'acl',
                     
                     'node_number',
                     'app_type',
                     'app_role',
                     
                     'cores',
                     'memory_mb',
                     'storage_mb',
                     'app_host',
                     'app_port',
                     'app_sectoken',            
                     ]
    validvalues = {}
    
    def __init__(self, name, 
                       state,
                       owner, 
                       acl, 
                       
                       node_number, 
                       app_type, 
                       app_role,

                       cores=1, 
                       memory_mb=None, 
                       storage_mb=None, 
                       app_host = None, 
                       app_port = None,
                       app_sectoken = None
                       ):
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.owner = owner
        self.acl = acl
        self.node_number = node_number
        self.app_type = app_type
        self.app_role = app_role
        
        self.cores = cores
        self.memory_mb = memory_mb
        self.storage_mb = storage_mb
        self.app_host = app_host
        self.app_port = app_port
        self.app_sectoken = app_sectoken


class Environment(InfoEntity):
    '''
    Represents the node/job-level environment needed to run a given user task. 
    Consists of task requirements like job runtime, disk space, cpucount, gpu
    Consists of job requirements like application software, network access, http cache, CVMFS, etc. 
    
    '''
    infokey = 'environment'
    infoattributes = ['name',
                     'state',
                     'owner',
                     'acl',
                     'packagelist',
                     'envmap',
                     'files'
                     ]
    validvalues = {}

    def __init__(self, name, state, owner, acl,  packagelist=[], files={}, envmap=[] ):
        '''
        Defines a new Environment object. 
              
        :param str name: The unique VC3 label for this environment.
        :param str owner:
        :param List str   packagelist:
        :param List local-name=remote-name files: Files to be included in the environment. (Files will be 
                                                base64 encoded.)
        :param Dict str envmap: 
        :rtype: Environment
        '''  
        self.log = logging.getLogger()
        self.name  = name
        self.state = state
        self.acl   = acl
        self.owner = owner
        self.packagelist = packagelist
        self.files = files
        self.envmap = envmap


class Request(InfoEntity):
    '''
    Represents and contains all information relevant to a concrete virtual cluster. 
    Contains sub-elements that reflect information from other Entities. 
    expiration:  Date or None   Time at which cluster should unconditionally do teardown if 
                                not actively terminated. 
        
    
    
        "jhover-req00001" : {
            "name" : "jhover-req00001",
            "expiration" : "2017-07-07:1730", 
            "cluster_state" : "new",
            "cluster_state_reason",
            "environment" : {
                        <Environment json>
                    },
            "allocation" : {
                        <Allocations>
                        },
            "policy" :  {
                    <policy>
                }
            "cluster" :  {
            
            },
            "nodeset": {
            
            }
             
            
            

        }
        
        :param str name:          Label for this request. 
        :param str state:         State of request
        :param str state_reason:  Error reporting for state
        :param str action:        Command from webportal (e.g. run, terminate, etc.)
        :param str cluster_state: State of virtual cluster
        :param str cluster_state_reason:  Primarily for error reporting.
        :param str allocations:   List of allocations that the request shoud utilize.
        :param str environments:  List of environments to install on top of the cluster.
        :param str policy:        Policy for utilizing the allocations. 
        :param str expiration:    Date YYYY-MM-DD,HH:MM:SS when this cluster expires and should be unconditionally terminated.    
        
    '''
    infokey = 'request'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'action',        # Command from webportal (run, terminate, etc.)
                     'state_reason',
                     'cluster_state', # State of virtual cluster this Request represents.
                     'cluster_state_reason',
                     'expiration',
                     'queuesconf',    # base64-encoded contents of factory queues.conf sections. 
                     'authconf',      # base64-encoded contents of factory auth.conf sections. 
                     'policy',        # name of policy to use to satisfy request
                     'allocations',   # list of allocations to satisfy this request
                     'cluster',       # contains cluster def, which includes nodeset descriptions
                     'environments',  # environment(s) to instantiate on nodesets.
                     'statusraw',     # raw dictionary of submissions for all factories+allocations.
                     'statusinfo'     # aggregated submission status
                     ]
    validvalues = {
                    'state' :['new', 
                              'validated', 
                              'configured', 
                              'pending', 
                              'growing', 
                              'running', 
                              'shrinking', 
                              'terminating', 
                              'terminated'],
                    } 
    
    
    def __init__(self, 
                 name, 
                 state, 
                 acl,
                 owner,
                 action = None,
                 state_reason = None,
                 cluster_state = "new",
                 cluster_state_reason = None,
                 expiration = None,
                 queuesconf = None,
                 authconf = None, 
                 cluster=None, 
                 policy = None, 
                 allocations = [], 
                 environments = [],
                 statusraw = None,
                 statusinfo = None 
                 ):
        # Common attributes
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner


        # Request-specific attributes
        self.action = action
        self.state_reason = state_reason
        self.expiration   = expiration
        self.cluster_state = cluster_state
        self.cluster_state_reason = cluster_state_reason
        self.queuesconf = queuesconf
        self.authconf = authconf
        self.statusraw = statusraw
        self.statusinfo = statusinfo
        
        # Composite attributes from other entities. 
        self.cluster = cluster
        self.allocations  = allocations
        self.policy       = policy
        self.environments = environments

        

class Factory(InfoEntity):
    '''
    Represents a VC3 factory (static or dynamic). 
        
    '''
    infokey = 'factory'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'authconfig',
                     'queuesconf',
                     ]
    validvalues = {}


    def __init__(self, name, state, acl, authconfig=None, queuesconfig=None ):
        '''
        Defines a new Factory object. 
              
        :param str name: The unique factory id.
        :param str owner:
        :param str authconfig: (base64encoded) contents of auth.conf   
        :param str queuesconfig:  (base64encoded) contents of auth.conf
        :rtype: Factory
        :return: Valid Factory object.  
        '''  
        self.log = logging.getLogger()

        self.name  = name  # i.e. factory-id
        self.state = state
        self.acl   = acl
        self.owner = owner
        self.authconfig = authconfig
        self.queuesconfig = queuesconfig
        
if __name__ == '__main__':
    pass
    

