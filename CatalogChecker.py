def check (catalog):
    #print "Catalog checking."
    for component in catalog.findall("*"):
        check_component(component)
        
def check_exists_and_unique (component, tag_name):
    tag = component.findall(tag_name)
    assert len(tag) == 1, "Component "+component.get("keyname")+" must have one and only one "+tag_name+". Got: "+str(tag) +" in "+str(component.find("homedirectory").text)
    tag = tag[0]
    assert check_ref(tag), "Empty "+tag_name+" found for component."
    
def check_can_get_schematic (component):
    eagledevice = component.findall("eagledevice")
    schematic = component.findall("schematic")
    
    assert (eagledevice is not None) or (schematic is not None), "Could not find eagledevice or schematic entry for component: "+component.get("keyname")
        
def check_ref (ref):
    vaild = ref is not None
    vaild = vaild and (ref != "")
    return vaild
        
def check_electrical_interfaces (component):
    #print "Checking interfaces"
    interfaces = component.findall("./electrical/interfaces/interface")
    keyname = component.get("keyname")
    if interfaces is None:
        return
    else:
        digital_wire_nets = []
        interface_names = []
        
        for interface in interfaces:
            name = interface.get("name")
            assert check_ref(name), "Electrical interface has no name in component: "+keyname
            assert name not in interface_names, "Cannot have two interfaces with the same name \""+name+"\" in component: "+keyname
            interface_names.append(name)
            
            interface_type = interface.get("type")
            assert check_ref(interface_type), "Electrical interface \""+name+"\" has no type in component: "+keyname

            if interface_type == "PowerInterface":
                net = interface.get("net")
                assert check_ref(net), "Power interface \""+name+"\" has bad or missing net in component: "+keyname
                voltage = interface.get("voltage")
                assert check_ref(voltage), "Power interface \""+name+"\" has missing voltage in component: "+keyname
                current = interface.get("current")
                assert check_ref(current), "Power interface \""+name+"\" has missing current in component: "+keyname
                output = interface.get("output", "False").upper() == "TRUE"
                input = interface.get("input", "False").upper() == "TRUE"
                #assert output != input, "Power interface \""+name+"\" has bad or missing input/output specification in component: "+keyname+". Needs to be input or output."
                assert input or output, "Power interface \""+name+"\" has bad or missing input/output specification in component: "+keyname+". Needs to be input or output."
            elif interface_type == "DigitalWireInterface":
                net = interface.get("net")
                assert check_ref(net), "Power interface \""+name+"\" has bad or missing net in component: "+keyname
                assert net not in digital_wire_nets, "DigitalWireInterface \""+name+"\" has duplicate digital wire net \""+net+"\" in component: "+keyname
                digital_wire_nets.append(net)
            elif interface_type == "I2CInterface":
                role = interface.get("role")
                assert check_ref(role), "I2CInterface interface \""+name+"\" has bad or missing role in component: "+keyname
                assert (role == "master") or (role == "slave"), "I2CInterface interface \""+name+"\" has bad role in component: "+keyname+". Meeds to be 'master' or 'slave' but is "+role+"."
                
        
def check_component (component):
    assert component.tag == "component", "Unexpected tag in catalog:"+str(component.tag)
    
    keyname = component.get("keyname")
    assert check_ref(keyname), "No keyname for component."
    assert keyname != "example-mounting-hole", "example-mounting-hole is not a vaild keyname."
    
    check_exists_and_unique(component, "name")
    check_exists_and_unique(component, "longname")
    check_exists_and_unique(component, "QA")
    check_exists_and_unique(component, "homedirectory")
    
    check_can_get_schematic(component)
    
    check_electrical_interfaces(component)
    
    
    
