from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/ethernet-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ethernet_interfaces = resolve('ethernet_interfaces')
    l_0_encapsulation_dot1q_interfaces = resolve('encapsulation_dot1q_interfaces')
    l_0_flexencap_interfaces = resolve('flexencap_interfaces')
    l_0_namespace = resolve('namespace')
    l_0_ethernet_interface_pvlan = resolve('ethernet_interface_pvlan')
    l_0_ethernet_interface_vlan_xlate = resolve('ethernet_interface_vlan_xlate')
    l_0_tcp_mss_clampings = resolve('tcp_mss_clampings')
    l_0_transceiver_settings = resolve('transceiver_settings')
    l_0_link_tracking_interfaces = resolve('link_tracking_interfaces')
    l_0_phone_interfaces = resolve('phone_interfaces')
    l_0_port_channel_interfaces = resolve('port_channel_interfaces')
    l_0_multicast_interfaces = resolve('multicast_interfaces')
    l_0_ethernet_interface_ipv4 = resolve('ethernet_interface_ipv4')
    l_0_port_channel_interface_ipv4 = resolve('port_channel_interface_ipv4')
    l_0_ip_nat_interfaces = resolve('ip_nat_interfaces')
    l_0_ethernet_interface_ipv6 = resolve('ethernet_interface_ipv6')
    l_0_port_channel_interface_ipv6 = resolve('port_channel_interface_ipv6')
    l_0_ethernet_interfaces_isis = resolve('ethernet_interfaces_isis')
    l_0_port_channel_interfaces_isis = resolve('port_channel_interfaces_isis')
    l_0_ethernet_interfaces_vrrp_details = resolve('ethernet_interfaces_vrrp_details')
    l_0_evpn_es_ethernet_interfaces = resolve('evpn_es_ethernet_interfaces')
    l_0_evpn_dfe_ethernet_interfaces = resolve('evpn_dfe_ethernet_interfaces')
    l_0_evpn_mpls_ethernet_interfaces = resolve('evpn_mpls_ethernet_interfaces')
    l_0_err_cor_enc_intfs = resolve('err_cor_enc_intfs')
    l_0_priority_intfs = resolve('priority_intfs')
    l_0_sync_e_interfaces = resolve('sync_e_interfaces')
    l_0_te_interfaces = resolve('te_interfaces')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.list_compress']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.list_compress' found.")
    try:
        t_3 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_4 = environment.filters['arista.avd.range_expand']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.range_expand' found.")
    try:
        t_5 = environment.filters['first']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'first' found.")
    try:
        t_6 = environment.filters['float']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'float' found.")
    try:
        t_7 = environment.filters['format']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'format' found.")
    try:
        t_8 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_9 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_9(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_10 = environment.filters['map']
    except KeyError:
        @internalcode
        def t_10(*unused):
            raise TemplateRuntimeError("No filter named 'map' found.")
    try:
        t_11 = environment.filters['selectattr']
    except KeyError:
        @internalcode
        def t_11(*unused):
            raise TemplateRuntimeError("No filter named 'selectattr' found.")
    try:
        t_12 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_12(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_12((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces)):
        pass
        yield '\n### Ethernet Interfaces\n\n#### Ethernet Interfaces Summary\n\n##### L2\n\n| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |\n| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |\n'
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            l_1_port_channel_interface_name = resolve('port_channel_interface_name')
            l_1_port_channel_interface = resolve('port_channel_interface')
            l_1_description = resolve('description')
            l_1_mode = resolve('mode')
            l_1_switchport_vlans = resolve('switchport_vlans')
            l_1_native_vlan = resolve('native_vlan')
            l_1_channel_group = resolve('channel_group')
            l_1_trunk_groups = resolve('trunk_groups')
            _loop_vars = {}
            pass
            if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id')):
                pass
                l_1_port_channel_interface_name = str_join(('Port-Channel', environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), ))
                _loop_vars['port_channel_interface_name'] = l_1_port_channel_interface_name
                l_1_port_channel_interface = t_5(environment, t_11(context, t_1((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), []), 'name', 'arista.avd.defined', (undefined(name='port_channel_interface_name') if l_1_port_channel_interface_name is missing else l_1_port_channel_interface_name)))
                _loop_vars['port_channel_interface'] = l_1_port_channel_interface
                if (((((((t_12(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'mode')) or t_12(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'access_vlan'))) or t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'allowed_vlan'))) or t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'native_vlan_tag'), True)) or t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'native_vlan'))) or t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'groups'))) or t_12(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'enabled'), True)) and ((not t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'type'))) or (t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'type')) and (environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'type') not in ['switched', 'routed'])))):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mode = t_1(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'mode'), '-')
                    _loop_vars['mode'] = l_1_mode
                    if (t_12(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'access_vlan')) or t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'allowed_vlan'))):
                        pass
                        l_1_switchport_vlans = []
                        _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                        if t_12(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'access_vlan')):
                            pass
                            context.call(environment.getattr((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans), 'append'), environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'access_vlan'), _loop_vars=_loop_vars)
                        if t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'allowed_vlan')):
                            pass
                            context.call(environment.getattr((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans), 'extend'), t_10(context, t_4(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'allowed_vlan')), 'int'), _loop_vars=_loop_vars)
                        if (undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans):
                            pass
                            l_1_switchport_vlans = t_2((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans))
                            _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                        else:
                            pass
                            l_1_switchport_vlans = environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'allowed_vlan')
                            _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                    if t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'native_vlan_tag'), True):
                        pass
                        l_1_native_vlan = 'tag'
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    else:
                        pass
                        l_1_native_vlan = t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'native_vlan'), '-')
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    l_1_channel_group = environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id')
                    _loop_vars['channel_group'] = l_1_channel_group
                    l_1_trunk_groups = t_8(context.eval_ctx, t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'switchport'), 'trunk'), 'groups'), ['-']), ', ')
                    _loop_vars['trunk_groups'] = l_1_trunk_groups
                    yield '| '
                    yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | *'
                    yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                    yield ' | *'
                    yield str(t_1((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans), '-'))
                    yield ' | *'
                    yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                    yield ' | *'
                    yield str((undefined(name='trunk_groups') if l_1_trunk_groups is missing else l_1_trunk_groups))
                    yield ' | '
                    yield str((undefined(name='channel_group') if l_1_channel_group is missing else l_1_channel_group))
                    yield ' |\n'
                elif t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'type'), 'switched'):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mode = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'mode'), '-')
                    _loop_vars['mode'] = l_1_mode
                    l_1_switchport_vlans = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'vlans'), '-')
                    _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                    if t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'native_vlan_tag'), True):
                        pass
                        l_1_native_vlan = 'tag'
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    else:
                        pass
                        l_1_native_vlan = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'native_vlan'), '-')
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    l_1_channel_group = environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id')
                    _loop_vars['channel_group'] = l_1_channel_group
                    l_1_trunk_groups = t_8(context.eval_ctx, t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'trunk_groups'), ['-']), ', ')
                    _loop_vars['trunk_groups'] = l_1_trunk_groups
                    yield '| '
                    yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | *'
                    yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                    yield ' | *'
                    yield str((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans))
                    yield ' | *'
                    yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                    yield ' | *'
                    yield str((undefined(name='trunk_groups') if l_1_trunk_groups is missing else l_1_trunk_groups))
                    yield ' | '
                    yield str((undefined(name='channel_group') if l_1_channel_group is missing else l_1_channel_group))
                    yield ' |\n'
            else:
                pass
                if (((((((t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'mode')) or t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'access_vlan'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'native_vlan_tag'), True)) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'native_vlan'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'groups'))) or t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'enabled'), True)) and ((not t_12(environment.getattr(l_1_ethernet_interface, 'type'))) or (t_12(environment.getattr(l_1_ethernet_interface, 'type')) and (environment.getattr(l_1_ethernet_interface, 'type') not in ['switched', 'routed'])))):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mode = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'mode'), '-')
                    _loop_vars['mode'] = l_1_mode
                    if (t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'access_vlan')) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan'))):
                        pass
                        l_1_switchport_vlans = []
                        _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                        if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'access_vlan')):
                            pass
                            context.call(environment.getattr((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans), 'append'), environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'access_vlan'), _loop_vars=_loop_vars)
                        if t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan')):
                            pass
                            context.call(environment.getattr((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans), 'extend'), t_10(context, t_4(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan')), 'int'), _loop_vars=_loop_vars)
                        if (undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans):
                            pass
                            l_1_switchport_vlans = t_2((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans))
                            _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                        elif t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan'), 'none'):
                            pass
                            l_1_switchport_vlans = environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan')
                            _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                    if t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'native_vlan_tag'), True):
                        pass
                        l_1_native_vlan = 'tag'
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    else:
                        pass
                        l_1_native_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'native_vlan'), '-')
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    l_1_trunk_groups = t_8(context.eval_ctx, t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'groups'), ['-']), ', ')
                    _loop_vars['trunk_groups'] = l_1_trunk_groups
                    yield '| '
                    yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | '
                    yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                    yield ' | '
                    yield str(t_1((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans), '-'))
                    yield ' | '
                    yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                    yield ' | '
                    yield str((undefined(name='trunk_groups') if l_1_trunk_groups is missing else l_1_trunk_groups))
                    yield ' | - |\n'
                elif t_12(environment.getattr(l_1_ethernet_interface, 'type'), 'switched'):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mode = t_1(environment.getattr(l_1_ethernet_interface, 'mode'), '-')
                    _loop_vars['mode'] = l_1_mode
                    l_1_switchport_vlans = t_1(environment.getattr(l_1_ethernet_interface, 'vlans'), '-')
                    _loop_vars['switchport_vlans'] = l_1_switchport_vlans
                    if t_12(environment.getattr(l_1_ethernet_interface, 'native_vlan_tag'), True):
                        pass
                        l_1_native_vlan = 'tag'
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    else:
                        pass
                        l_1_native_vlan = t_1(environment.getattr(l_1_ethernet_interface, 'native_vlan'), '-')
                        _loop_vars['native_vlan'] = l_1_native_vlan
                    l_1_trunk_groups = t_8(context.eval_ctx, t_1(environment.getattr(l_1_ethernet_interface, 'trunk_groups'), ['-']), ', ')
                    _loop_vars['trunk_groups'] = l_1_trunk_groups
                    yield '| '
                    yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | '
                    yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                    yield ' | '
                    yield str((undefined(name='switchport_vlans') if l_1_switchport_vlans is missing else l_1_switchport_vlans))
                    yield ' | '
                    yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                    yield ' | '
                    yield str((undefined(name='trunk_groups') if l_1_trunk_groups is missing else l_1_trunk_groups))
                    yield ' | - |\n'
        l_1_ethernet_interface = l_1_port_channel_interface_name = l_1_port_channel_interface = l_1_description = l_1_mode = l_1_switchport_vlans = l_1_native_vlan = l_1_channel_group = l_1_trunk_groups = missing
        yield '\n*Inherited from Port-Channel Interface\n'
        l_0_encapsulation_dot1q_interfaces = []
        context.vars['encapsulation_dot1q_interfaces'] = l_0_encapsulation_dot1q_interfaces
        context.exported_vars.add('encapsulation_dot1q_interfaces')
        l_0_flexencap_interfaces = []
        context.vars['flexencap_interfaces'] = l_0_flexencap_interfaces
        context.exported_vars.add('flexencap_interfaces')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'vlan')):
                pass
                context.call(environment.getattr((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
            elif t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'encapsulation')):
                pass
                context.call(environment.getattr((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
            elif (t_1(environment.getattr(l_1_ethernet_interface, 'type')) in ['l3dot1q', 'l2dot1q']):
                pass
                if t_12(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q_vlan')):
                    pass
                    context.call(environment.getattr((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
                elif t_12(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan')):
                    pass
                    context.call(environment.getattr((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces)) > 0):
            pass
            yield '\n##### Encapsulation Dot1q Interfaces\n\n| Interface | Description | Vlan ID | Dot1q VLAN Tag | Dot1q Inner VLAN Tag |\n| --------- | ----------- | ------- | -------------- | -------------------- |\n'
            for l_1_ethernet_interface in (undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces):
                l_1_description = l_1_vlan_id = l_1_encapsulation_dot1q_vlan = l_1_encapsulation_dot1q_inner_vlan = missing
                _loop_vars = {}
                pass
                l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_vlan_id = t_1(environment.getattr(l_1_ethernet_interface, 'vlan_id'), '-')
                _loop_vars['vlan_id'] = l_1_vlan_id
                l_1_encapsulation_dot1q_vlan = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'vlan'), environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q_vlan'), '-')
                _loop_vars['encapsulation_dot1q_vlan'] = l_1_encapsulation_dot1q_vlan
                l_1_encapsulation_dot1q_inner_vlan = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'inner_vlan'), '-')
                _loop_vars['encapsulation_dot1q_inner_vlan'] = l_1_encapsulation_dot1q_inner_vlan
                yield '| '
                yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='vlan_id') if l_1_vlan_id is missing else l_1_vlan_id))
                yield ' | '
                yield str((undefined(name='encapsulation_dot1q_vlan') if l_1_encapsulation_dot1q_vlan is missing else l_1_encapsulation_dot1q_vlan))
                yield ' | '
                yield str((undefined(name='encapsulation_dot1q_inner_vlan') if l_1_encapsulation_dot1q_inner_vlan is missing else l_1_encapsulation_dot1q_inner_vlan))
                yield ' |\n'
            l_1_ethernet_interface = l_1_description = l_1_vlan_id = l_1_encapsulation_dot1q_vlan = l_1_encapsulation_dot1q_inner_vlan = missing
        if (t_9((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces)) > 0):
            pass
            yield '\n##### Flexible Encapsulation Interfaces\n\n| Interface | Description | Vlan ID | Client Encapsulation | Client Inner Encapsulation | Client VLAN | Client Outer VLAN Tag | Client Inner VLAN Tag | Network Encapsulation | Network Inner Encapsulation | Network VLAN | Network Outer VLAN Tag | Network Inner VLAN Tag |\n| --------- | ----------- | ------- | --------------- | --------------------- | ----------- | --------------------- | --------------------- | ---------------- | ---------------------- |------------ | ---------------------- | ---------------------- |\n'
            for l_1_ethernet_interface in (undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces):
                l_1_client_inner_encapsulation = resolve('client_inner_encapsulation')
                l_1_client_vlan = resolve('client_vlan')
                l_1_client_outer_vlan = resolve('client_outer_vlan')
                l_1_client_inner_vlan = resolve('client_inner_vlan')
                l_1_network_inner_encapsulation = resolve('network_inner_encapsulation')
                l_1_network_vlan = resolve('network_vlan')
                l_1_network_outer_vlan = resolve('network_outer_vlan')
                l_1_network_inner_vlan = resolve('network_inner_vlan')
                l_1_description = l_1_vlan_id = l_1_client_encapsulation = l_1_network_encapsulation = missing
                _loop_vars = {}
                pass
                l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_vlan_id = t_1(environment.getattr(l_1_ethernet_interface, 'vlan_id'), '-')
                _loop_vars['vlan_id'] = l_1_vlan_id
                l_1_client_encapsulation = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'encapsulation'), '-')
                _loop_vars['client_encapsulation'] = l_1_client_encapsulation
                if ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) == '-'):
                    pass
                    if t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q')):
                        pass
                        l_1_client_encapsulation = 'dot1q'
                        _loop_vars['client_encapsulation'] = l_1_client_encapsulation
                    elif t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'unmatched'), True):
                        pass
                        l_1_client_encapsulation = 'unmatched'
                        _loop_vars['client_encapsulation'] = l_1_client_encapsulation
                if ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) in ['dot1q', 'dot1ad']):
                    pass
                    l_1_client_inner_encapsulation = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'inner_encapsulation'), '-')
                    _loop_vars['client_inner_encapsulation'] = l_1_client_inner_encapsulation
                    l_1_client_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'vlan'), environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'vlan'))
                    _loop_vars['client_vlan'] = l_1_client_vlan
                    l_1_client_outer_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'outer_vlan'), environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'outer'))
                    _loop_vars['client_outer_vlan'] = l_1_client_outer_vlan
                    l_1_client_inner_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'inner_vlan'), environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'inner'))
                    _loop_vars['client_inner_vlan'] = l_1_client_inner_vlan
                l_1_network_encapsulation = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'encapsulation'), '-')
                _loop_vars['network_encapsulation'] = l_1_network_encapsulation
                if ((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) == '-'):
                    pass
                    if t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q')):
                        pass
                        l_1_network_encapsulation = 'dot1q'
                        _loop_vars['network_encapsulation'] = l_1_network_encapsulation
                    elif t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'client'), True):
                        pass
                        l_1_network_encapsulation = 'client'
                        _loop_vars['network_encapsulation'] = l_1_network_encapsulation
                if ((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) in ['dot1q', 'dot1ad']):
                    pass
                    l_1_network_inner_encapsulation = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'inner_encapsulation'), '-')
                    _loop_vars['network_inner_encapsulation'] = l_1_network_inner_encapsulation
                    l_1_network_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'vlan'), environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'vlan'))
                    _loop_vars['network_vlan'] = l_1_network_vlan
                    l_1_network_outer_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'outer_vlan'), environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'outer'))
                    _loop_vars['network_outer_vlan'] = l_1_network_outer_vlan
                    l_1_network_inner_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'inner_vlan'), environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'inner'))
                    _loop_vars['network_inner_vlan'] = l_1_network_inner_vlan
                yield '| '
                yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='vlan_id') if l_1_vlan_id is missing else l_1_vlan_id))
                yield ' | '
                yield str((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation))
                yield ' | '
                yield str(t_1((undefined(name='client_inner_encapsulation') if l_1_client_inner_encapsulation is missing else l_1_client_inner_encapsulation), '-'))
                yield ' | '
                yield str(t_1((undefined(name='client_vlan') if l_1_client_vlan is missing else l_1_client_vlan), '-'))
                yield ' | '
                yield str(t_1((undefined(name='client_outer_vlan') if l_1_client_outer_vlan is missing else l_1_client_outer_vlan), '-'))
                yield ' | '
                yield str(t_1((undefined(name='client_inner_vlan') if l_1_client_inner_vlan is missing else l_1_client_inner_vlan), '-'))
                yield ' | '
                yield str((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation))
                yield ' | '
                yield str(t_1((undefined(name='network_inner_encapsulation') if l_1_network_inner_encapsulation is missing else l_1_network_inner_encapsulation), '-'))
                yield ' | '
                yield str(t_1((undefined(name='network_vlan') if l_1_network_vlan is missing else l_1_network_vlan), '-'))
                yield ' | '
                yield str(t_1((undefined(name='network_outer_vlan') if l_1_network_outer_vlan is missing else l_1_network_outer_vlan), '-'))
                yield ' | '
                yield str(t_1((undefined(name='network_inner_vlan') if l_1_network_inner_vlan is missing else l_1_network_inner_vlan), '-'))
                yield ' |\n'
            l_1_ethernet_interface = l_1_description = l_1_vlan_id = l_1_client_encapsulation = l_1_client_inner_encapsulation = l_1_client_vlan = l_1_client_outer_vlan = l_1_client_inner_vlan = l_1_network_encapsulation = l_1_network_inner_encapsulation = l_1_network_vlan = l_1_network_outer_vlan = l_1_network_inner_vlan = missing
        l_0_ethernet_interface_pvlan = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['ethernet_interface_pvlan'] = l_0_ethernet_interface_pvlan
        context.exported_vars.add('ethernet_interface_pvlan')
        if not isinstance(l_0_ethernet_interface_pvlan, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_ethernet_interface_pvlan['configured'] = False
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (((t_12(environment.getattr(l_1_ethernet_interface, 'pvlan_mapping')) or t_12(environment.getattr(l_1_ethernet_interface, 'trunk_private_vlan_secondary'))) or t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'pvlan_mapping'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'private_vlan_secondary'))):
                pass
                if not isinstance(l_0_ethernet_interface_pvlan, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_ethernet_interface_pvlan['configured'] = True
                break
        l_1_ethernet_interface = missing
        if (environment.getattr((undefined(name='ethernet_interface_pvlan') if l_0_ethernet_interface_pvlan is missing else l_0_ethernet_interface_pvlan), 'configured') == True):
            pass
            yield '\n##### Private VLAN\n\n| Interface | PVLAN Mapping | Secondary Trunk |\n| --------- | ------------- | ----------------|\n'
            for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
                l_1_row_pvlan_mapping = l_1_row_trunk_private_vlan_secondary = missing
                _loop_vars = {}
                pass
                l_1_row_pvlan_mapping = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'pvlan_mapping'), environment.getattr(l_1_ethernet_interface, 'pvlan_mapping'), '-')
                _loop_vars['row_pvlan_mapping'] = l_1_row_pvlan_mapping
                l_1_row_trunk_private_vlan_secondary = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'private_vlan_secondary'), environment.getattr(l_1_ethernet_interface, 'trunk_private_vlan_secondary'), '-')
                _loop_vars['row_trunk_private_vlan_secondary'] = l_1_row_trunk_private_vlan_secondary
                if (((undefined(name='row_pvlan_mapping') if l_1_row_pvlan_mapping is missing else l_1_row_pvlan_mapping) != '-') or ((undefined(name='row_trunk_private_vlan_secondary') if l_1_row_trunk_private_vlan_secondary is missing else l_1_row_trunk_private_vlan_secondary) != '-')):
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='row_pvlan_mapping') if l_1_row_pvlan_mapping is missing else l_1_row_pvlan_mapping))
                    yield ' | '
                    yield str((undefined(name='row_trunk_private_vlan_secondary') if l_1_row_trunk_private_vlan_secondary is missing else l_1_row_trunk_private_vlan_secondary))
                    yield ' |\n'
            l_1_ethernet_interface = l_1_row_pvlan_mapping = l_1_row_trunk_private_vlan_secondary = missing
        l_0_ethernet_interface_vlan_xlate = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['ethernet_interface_vlan_xlate'] = l_0_ethernet_interface_vlan_xlate
        context.exported_vars.add('ethernet_interface_vlan_xlate')
        if not isinstance(l_0_ethernet_interface_vlan_xlate, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_ethernet_interface_vlan_xlate['configured'] = False
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations')) or t_12(environment.getattr(l_1_ethernet_interface, 'vlan_translations'))):
                pass
                if not isinstance(l_0_ethernet_interface_vlan_xlate, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_ethernet_interface_vlan_xlate['configured'] = True
                break
        l_1_ethernet_interface = missing
        if (environment.getattr((undefined(name='ethernet_interface_vlan_xlate') if l_0_ethernet_interface_vlan_xlate is missing else l_0_ethernet_interface_vlan_xlate), 'configured') == True):
            pass
            yield '\n##### VLAN Translations\n\n| Interface | Direction | From VLAN ID(s) | To VLAN ID | From Inner VLAN ID | To Inner VLAN ID | Network | Dot1q-tunnel |\n| --------- | --------- | --------------- | ---------- | ------------------ | ---------------- | ------- | ------------ |\n'
            for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
                _loop_vars = {}
                pass
                if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations')):
                    pass
                    for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_both'), 'from'):
                        _loop_vars = {}
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | both | '
                        yield str(environment.getattr(l_2_vlan_translation, 'from'))
                        yield ' | '
                        yield str(environment.getattr(l_2_vlan_translation, 'to'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), '-'))
                        yield ' | - | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'network'), '-'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), '-'))
                        yield ' |\n'
                    l_2_vlan_translation = missing
                    for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_in'), 'from'):
                        _loop_vars = {}
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | in | '
                        yield str(environment.getattr(l_2_vlan_translation, 'from'))
                        yield ' | '
                        yield str(environment.getattr(l_2_vlan_translation, 'to'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), '-'))
                        yield ' | - | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'network'), '-'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), '-'))
                        yield ' |\n'
                    l_2_vlan_translation = missing
                    for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_out'), 'from'):
                        l_2_dot1q_tunnel = resolve('dot1q_tunnel')
                        l_2_to_vlan_id = resolve('to_vlan_id')
                        _loop_vars = {}
                        pass
                        if t_12(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to')):
                            pass
                            l_2_dot1q_tunnel = 'True'
                            _loop_vars['dot1q_tunnel'] = l_2_dot1q_tunnel
                            l_2_to_vlan_id = environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to')
                            _loop_vars['to_vlan_id'] = l_2_to_vlan_id
                        else:
                            pass
                            l_2_to_vlan_id = t_1(environment.getattr(l_2_vlan_translation, 'to'), '-')
                            _loop_vars['to_vlan_id'] = l_2_to_vlan_id
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | out | '
                        yield str(environment.getattr(l_2_vlan_translation, 'from'))
                        yield ' | '
                        yield str((undefined(name='to_vlan_id') if l_2_to_vlan_id is missing else l_2_to_vlan_id))
                        yield ' | - | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'inner_vlan_to'), '-'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_vlan_translation, 'network'), '-'))
                        yield ' | '
                        yield str(t_1((undefined(name='dot1q_tunnel') if l_2_dot1q_tunnel is missing else l_2_dot1q_tunnel), '-'))
                        yield ' |\n'
                    l_2_vlan_translation = l_2_dot1q_tunnel = l_2_to_vlan_id = missing
                elif t_12(environment.getattr(l_1_ethernet_interface, 'vlan_translations')):
                    pass
                    for l_2_vlan_translation in t_3(environment.getattr(l_1_ethernet_interface, 'vlan_translations')):
                        l_2_row_direction = resolve('row_direction')
                        _loop_vars = {}
                        pass
                        if (t_12(environment.getattr(l_2_vlan_translation, 'from')) and t_12(environment.getattr(l_2_vlan_translation, 'to'))):
                            pass
                            l_2_row_direction = t_1(environment.getattr(l_2_vlan_translation, 'direction'), 'both')
                            _loop_vars['row_direction'] = l_2_row_direction
                            yield '| '
                            yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                            yield ' | '
                            yield str((undefined(name='row_direction') if l_2_row_direction is missing else l_2_row_direction))
                            yield ' | '
                            yield str(environment.getattr(l_2_vlan_translation, 'from'))
                            yield ' | '
                            yield str(environment.getattr(l_2_vlan_translation, 'to'))
                            yield ' | - | - | - | - |\n'
                    l_2_vlan_translation = l_2_row_direction = missing
            l_1_ethernet_interface = missing
        l_0_tcp_mss_clampings = []
        context.vars['tcp_mss_clampings'] = l_0_tcp_mss_clampings
        context.exported_vars.add('tcp_mss_clampings')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling')):
                pass
                context.call(environment.getattr((undefined(name='tcp_mss_clampings') if l_0_tcp_mss_clampings is missing else l_0_tcp_mss_clampings), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='tcp_mss_clampings') if l_0_tcp_mss_clampings is missing else l_0_tcp_mss_clampings)) > 0):
            pass
            yield '\n##### TCP MSS Clamping\n\n| Interface | Ipv4 Segment Size | Ipv6 Segment Size | Direction |\n| --------- | ----------------- | ----------------- | --------- |\n'
            for l_1_tcp_mss_clamping in t_3((undefined(name='tcp_mss_clampings') if l_0_tcp_mss_clampings is missing else l_0_tcp_mss_clampings), 'name'):
                l_1_ipv4_segment_size = resolve('ipv4_segment_size')
                l_1_ipv6_segment_size = resolve('ipv6_segment_size')
                l_1_interface = missing
                _loop_vars = {}
                pass
                l_1_interface = environment.getattr(l_1_tcp_mss_clamping, 'name')
                _loop_vars['interface'] = l_1_interface
                if t_12(environment.getattr(environment.getattr(l_1_tcp_mss_clamping, 'tcp_mss_ceiling'), 'ipv4_segment_size')):
                    pass
                    l_1_ipv4_segment_size = environment.getattr(environment.getattr(l_1_tcp_mss_clamping, 'tcp_mss_ceiling'), 'ipv4_segment_size')
                    _loop_vars['ipv4_segment_size'] = l_1_ipv4_segment_size
                if t_12(environment.getattr(environment.getattr(l_1_tcp_mss_clamping, 'tcp_mss_ceiling'), 'ipv6_segment_size')):
                    pass
                    l_1_ipv6_segment_size = environment.getattr(environment.getattr(l_1_tcp_mss_clamping, 'tcp_mss_ceiling'), 'ipv6_segment_size')
                    _loop_vars['ipv6_segment_size'] = l_1_ipv6_segment_size
                yield '| '
                yield str((undefined(name='interface') if l_1_interface is missing else l_1_interface))
                yield ' | '
                yield str(t_1((undefined(name='ipv4_segment_size') if l_1_ipv4_segment_size is missing else l_1_ipv4_segment_size), '-'))
                yield ' | '
                yield str(t_1((undefined(name='ipv6_segment_size') if l_1_ipv6_segment_size is missing else l_1_ipv6_segment_size), '-'))
                yield ' | '
                yield str(t_1(environment.getattr(environment.getattr(l_1_tcp_mss_clamping, 'tcp_mss_ceiling'), 'direction'), '-'))
                yield ' |\n'
            l_1_tcp_mss_clamping = l_1_interface = l_1_ipv4_segment_size = l_1_ipv6_segment_size = missing
        l_0_transceiver_settings = []
        context.vars['transceiver_settings'] = l_0_transceiver_settings
        context.exported_vars.add('transceiver_settings')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'transceiver')):
                pass
                context.call(environment.getattr((undefined(name='transceiver_settings') if l_0_transceiver_settings is missing else l_0_transceiver_settings), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='transceiver_settings') if l_0_transceiver_settings is missing else l_0_transceiver_settings)) > 0):
            pass
            yield '\n##### Transceiver Settings\n\n| Interface | Transceiver Frequency | Media Override |\n| --------- | --------------------- | -------------- |\n'
            for l_1_transceiver_setting in t_3((undefined(name='transceiver_settings') if l_0_transceiver_settings is missing else l_0_transceiver_settings), 'name'):
                l_1_frequency = resolve('frequency')
                l_1_interface = l_1_m_override = missing
                _loop_vars = {}
                pass
                l_1_interface = environment.getattr(l_1_transceiver_setting, 'name')
                _loop_vars['interface'] = l_1_interface
                if t_12(environment.getattr(environment.getattr(l_1_transceiver_setting, 'transceiver'), 'frequency')):
                    pass
                    l_1_frequency = t_7('%.3f', t_6(environment.getattr(environment.getattr(l_1_transceiver_setting, 'transceiver'), 'frequency')))
                    _loop_vars['frequency'] = l_1_frequency
                    if t_12(environment.getattr(environment.getattr(l_1_transceiver_setting, 'transceiver'), 'frequency_unit')):
                        pass
                        l_1_frequency = str_join(((undefined(name='frequency') if l_1_frequency is missing else l_1_frequency), ' ', environment.getattr(environment.getattr(l_1_transceiver_setting, 'transceiver'), 'frequency_unit'), ))
                        _loop_vars['frequency'] = l_1_frequency
                else:
                    pass
                    l_1_frequency = '-'
                    _loop_vars['frequency'] = l_1_frequency
                l_1_m_override = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_transceiver_setting, 'transceiver'), 'media'), 'override'), '-')
                _loop_vars['m_override'] = l_1_m_override
                yield '| '
                yield str((undefined(name='interface') if l_1_interface is missing else l_1_interface))
                yield ' | '
                yield str((undefined(name='frequency') if l_1_frequency is missing else l_1_frequency))
                yield ' | '
                yield str((undefined(name='m_override') if l_1_m_override is missing else l_1_m_override))
                yield ' |\n'
            l_1_transceiver_setting = l_1_interface = l_1_frequency = l_1_m_override = missing
        l_0_link_tracking_interfaces = []
        context.vars['link_tracking_interfaces'] = l_0_link_tracking_interfaces
        context.exported_vars.add('link_tracking_interfaces')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'link_tracking_groups')):
                pass
                context.call(environment.getattr((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces)) > 0):
            pass
            yield '\n##### Link Tracking Groups\n\n| Interface | Group Name | Direction |\n| --------- | ---------- | --------- |\n'
            for l_1_link_tracking_interface in (undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces):
                _loop_vars = {}
                pass
                for l_2_link_tracking_group in t_3(environment.getattr(l_1_link_tracking_interface, 'link_tracking_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    if (t_12(environment.getattr(l_2_link_tracking_group, 'name')) and t_12(environment.getattr(l_2_link_tracking_group, 'direction'))):
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_link_tracking_interface, 'name'))
                        yield ' | '
                        yield str(environment.getattr(l_2_link_tracking_group, 'name'))
                        yield ' | '
                        yield str(environment.getattr(l_2_link_tracking_group, 'direction'))
                        yield ' |\n'
                l_2_link_tracking_group = missing
                if (t_12(environment.getattr(environment.getattr(l_1_link_tracking_interface, 'link_tracking'), 'direction')) and t_12(environment.getattr(environment.getattr(l_1_link_tracking_interface, 'link_tracking'), 'groups'))):
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_link_tracking_interface, 'name'))
                    yield ' | '
                    yield str(t_8(context.eval_ctx, environment.getattr(environment.getattr(l_1_link_tracking_interface, 'link_tracking'), 'groups'), ', '))
                    yield ' | '
                    yield str(environment.getattr(environment.getattr(l_1_link_tracking_interface, 'link_tracking'), 'direction'))
                    yield ' |\n'
            l_1_link_tracking_interface = missing
        l_0_phone_interfaces = []
        context.vars['phone_interfaces'] = l_0_phone_interfaces
        context.exported_vars.add('phone_interfaces')
        for l_1_interface in (t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name') + t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name')):
            _loop_vars = {}
            pass
            if (t_12(environment.getattr(environment.getattr(l_1_interface, 'switchport'), 'phone')) or t_12(environment.getattr(l_1_interface, 'phone'))):
                pass
                context.call(environment.getattr((undefined(name='phone_interfaces') if l_0_phone_interfaces is missing else l_0_phone_interfaces), 'append'), l_1_interface, _loop_vars=_loop_vars)
        l_1_interface = missing
        if (t_9((undefined(name='phone_interfaces') if l_0_phone_interfaces is missing else l_0_phone_interfaces)) > 0):
            pass
            yield '\n##### Phone Interfaces\n\n| Interface | Mode | Native VLAN | Phone VLAN | Phone VLAN Mode |\n| --------- | ---- | ----------- | ---------- | --------------- |\n'
            for l_1_phone_interface in (undefined(name='phone_interfaces') if l_0_phone_interfaces is missing else l_0_phone_interfaces):
                l_1_mode = l_1_native_vlan = l_1_phone_vlan = l_1_phone_vlan_mode = missing
                _loop_vars = {}
                pass
                l_1_mode = t_1(environment.getattr(environment.getattr(l_1_phone_interface, 'switchport'), 'mode'), environment.getattr(l_1_phone_interface, 'mode'), '-')
                _loop_vars['mode'] = l_1_mode
                l_1_native_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_phone_interface, 'switchport'), 'trunk'), 'native_vlan'), environment.getattr(l_1_phone_interface, 'native_vlan'), '-')
                _loop_vars['native_vlan'] = l_1_native_vlan
                l_1_phone_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_phone_interface, 'switchport'), 'phone'), 'vlan'), environment.getattr(environment.getattr(l_1_phone_interface, 'phone'), 'vlan'), '-')
                _loop_vars['phone_vlan'] = l_1_phone_vlan
                l_1_phone_vlan_mode = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_phone_interface, 'switchport'), 'phone'), 'trunk'), environment.getattr(environment.getattr(l_1_phone_interface, 'phone'), 'trunk'), '-')
                _loop_vars['phone_vlan_mode'] = l_1_phone_vlan_mode
                yield '| '
                yield str(environment.getattr(l_1_phone_interface, 'name'))
                yield ' | '
                yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                yield ' | '
                yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                yield ' | '
                yield str((undefined(name='phone_vlan') if l_1_phone_vlan is missing else l_1_phone_vlan))
                yield ' | '
                yield str((undefined(name='phone_vlan_mode') if l_1_phone_vlan_mode is missing else l_1_phone_vlan_mode))
                yield ' |\n'
            l_1_phone_interface = l_1_mode = l_1_native_vlan = l_1_phone_vlan = l_1_phone_vlan_mode = missing
        l_0_multicast_interfaces = []
        context.vars['multicast_interfaces'] = l_0_multicast_interfaces
        context.exported_vars.add('multicast_interfaces')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'multicast')):
                pass
                context.call(environment.getattr((undefined(name='multicast_interfaces') if l_0_multicast_interfaces is missing else l_0_multicast_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='multicast_interfaces') if l_0_multicast_interfaces is missing else l_0_multicast_interfaces)) > 0):
            pass
            yield '\n##### Multicast Routing\n\n| Interface | IP Version | Static Routes Allowed | Multicast Boundaries |\n| --------- | ---------- | --------------------- | -------------------- |\n'
            for l_1_multicast_interface in (undefined(name='multicast_interfaces') if l_0_multicast_interfaces is missing else l_0_multicast_interfaces):
                l_1_static = resolve('static')
                l_1_boundaries = resolve('boundaries')
                _loop_vars = {}
                pass
                if t_12(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv4')):
                    pass
                    l_1_static = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv4'), 'static'), '-')
                    _loop_vars['static'] = l_1_static
                    if t_12(environment.getattr(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv4'), 'boundaries')):
                        pass
                        l_1_boundaries = t_8(context.eval_ctx, t_10(context, t_11(context, environment.getattr(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv4'), 'boundaries'), 'boundary', 'arista.avd.defined'), attribute='boundary'), ', ')
                        _loop_vars['boundaries'] = l_1_boundaries
                    else:
                        pass
                        l_1_boundaries = '-'
                        _loop_vars['boundaries'] = l_1_boundaries
                    yield '| '
                    yield str(environment.getattr(l_1_multicast_interface, 'name'))
                    yield ' | IPv4 | '
                    yield str((undefined(name='static') if l_1_static is missing else l_1_static))
                    yield ' | '
                    yield str((undefined(name='boundaries') if l_1_boundaries is missing else l_1_boundaries))
                    yield ' |\n'
                if t_12(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv6')):
                    pass
                    l_1_static = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv6'), 'static'), '-')
                    _loop_vars['static'] = l_1_static
                    if t_12(environment.getattr(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv6'), 'boundaries')):
                        pass
                        l_1_boundaries = t_8(context.eval_ctx, t_10(context, t_11(context, environment.getattr(environment.getattr(environment.getattr(l_1_multicast_interface, 'multicast'), 'ipv6'), 'boundaries'), 'boundary', 'arista.avd.defined'), attribute='boundary'), ', ')
                        _loop_vars['boundaries'] = l_1_boundaries
                    else:
                        pass
                        l_1_boundaries = '-'
                        _loop_vars['boundaries'] = l_1_boundaries
                    yield '| '
                    yield str(environment.getattr(l_1_multicast_interface, 'name'))
                    yield ' | IPv6 | '
                    yield str((undefined(name='static') if l_1_static is missing else l_1_static))
                    yield ' | '
                    yield str((undefined(name='boundaries') if l_1_boundaries is missing else l_1_boundaries))
                    yield ' |\n'
            l_1_multicast_interface = l_1_static = l_1_boundaries = missing
        l_0_ethernet_interface_ipv4 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['ethernet_interface_ipv4'] = l_0_ethernet_interface_ipv4
        context.exported_vars.add('ethernet_interface_ipv4')
        if not isinstance(l_0_ethernet_interface_ipv4, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_ethernet_interface_ipv4['configured'] = False
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'ip_address')):
                pass
                if not isinstance(l_0_ethernet_interface_ipv4, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_ethernet_interface_ipv4['configured'] = True
                break
        l_1_ethernet_interface = missing
        l_0_port_channel_interface_ipv4 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_ipv4'] = l_0_port_channel_interface_ipv4
        context.exported_vars.add('port_channel_interface_ipv4')
        if not isinstance(l_0_port_channel_interface_ipv4, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_ipv4['configured'] = False
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_port_channel_interface, 'ip_address')):
                pass
                if not isinstance(l_0_port_channel_interface_ipv4, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_ipv4['configured'] = True
                break
        l_1_port_channel_interface = missing
        if ((environment.getattr((undefined(name='ethernet_interface_ipv4') if l_0_ethernet_interface_ipv4 is missing else l_0_ethernet_interface_ipv4), 'configured') == True) or (environment.getattr((undefined(name='port_channel_interface_ipv4') if l_0_port_channel_interface_ipv4 is missing else l_0_port_channel_interface_ipv4), 'configured') == True)):
            pass
            yield '\n##### IPv4\n\n| Interface | Description | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |\n| --------- | ----------- | ------------- | ---------- | ----| ---- | -------- | ------ | ------- |\n'
            for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
                l_1_port_channel_interface_name = resolve('port_channel_interface_name')
                l_1_port_channel_interface = resolve('port_channel_interface')
                l_1_description = resolve('description')
                l_1_channel_group = resolve('channel_group')
                l_1_ip_address = resolve('ip_address')
                l_1_vrf = resolve('vrf')
                l_1_mtu = resolve('mtu')
                l_1_shutdown = resolve('shutdown')
                l_1_acl_in = resolve('acl_in')
                l_1_acl_out = resolve('acl_out')
                _loop_vars = {}
                pass
                if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id')):
                    pass
                    l_1_port_channel_interface_name = str_join(('Port-Channel', environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), ))
                    _loop_vars['port_channel_interface_name'] = l_1_port_channel_interface_name
                    l_1_port_channel_interface = t_5(environment, t_11(context, t_1((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), []), 'name', 'arista.avd.defined', (undefined(name='port_channel_interface_name') if l_1_port_channel_interface_name is missing else l_1_port_channel_interface_name)))
                    _loop_vars['port_channel_interface'] = l_1_port_channel_interface
                    if t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ip_address')):
                        pass
                        l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                        _loop_vars['description'] = l_1_description
                        l_1_channel_group = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), '-')
                        _loop_vars['channel_group'] = l_1_channel_group
                        l_1_ip_address = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ip_address'), '-')
                        _loop_vars['ip_address'] = l_1_ip_address
                        l_1_vrf = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'vrf'), '*default')
                        _loop_vars['vrf'] = l_1_vrf
                        l_1_mtu = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'mtu'), '*-')
                        _loop_vars['mtu'] = l_1_mtu
                        l_1_shutdown = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'shutdown'), '*-')
                        _loop_vars['shutdown'] = l_1_shutdown
                        l_1_acl_in = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'access_group_in'), '*-')
                        _loop_vars['acl_in'] = l_1_acl_in
                        l_1_acl_out = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'access_group_out'), '*-')
                        _loop_vars['acl_out'] = l_1_acl_out
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                        yield ' | '
                        yield str((undefined(name='channel_group') if l_1_channel_group is missing else l_1_channel_group))
                        yield ' | *'
                        yield str((undefined(name='ip_address') if l_1_ip_address is missing else l_1_ip_address))
                        yield ' | *'
                        yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                        yield ' | *'
                        yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                        yield ' | *'
                        yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                        yield ' | *'
                        yield str((undefined(name='acl_in') if l_1_acl_in is missing else l_1_acl_in))
                        yield ' | *'
                        yield str((undefined(name='acl_out') if l_1_acl_out is missing else l_1_acl_out))
                        yield ' |\n'
                else:
                    pass
                    if t_12(environment.getattr(l_1_ethernet_interface, 'ip_address')):
                        pass
                        l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                        _loop_vars['description'] = l_1_description
                        l_1_ip_address = t_1(environment.getattr(l_1_ethernet_interface, 'ip_address'), '-')
                        _loop_vars['ip_address'] = l_1_ip_address
                        l_1_vrf = t_1(environment.getattr(l_1_ethernet_interface, 'vrf'), 'default')
                        _loop_vars['vrf'] = l_1_vrf
                        l_1_mtu = t_1(environment.getattr(l_1_ethernet_interface, 'mtu'), '-')
                        _loop_vars['mtu'] = l_1_mtu
                        l_1_shutdown = t_1(environment.getattr(l_1_ethernet_interface, 'shutdown'), '-')
                        _loop_vars['shutdown'] = l_1_shutdown
                        l_1_acl_in = t_1(environment.getattr(l_1_ethernet_interface, 'access_group_in'), '-')
                        _loop_vars['acl_in'] = l_1_acl_in
                        l_1_acl_out = t_1(environment.getattr(l_1_ethernet_interface, 'access_group_out'), '-')
                        _loop_vars['acl_out'] = l_1_acl_out
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                        yield ' | - | '
                        yield str((undefined(name='ip_address') if l_1_ip_address is missing else l_1_ip_address))
                        yield ' | '
                        yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                        yield ' | '
                        yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                        yield ' | '
                        yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                        yield ' | '
                        yield str((undefined(name='acl_in') if l_1_acl_in is missing else l_1_acl_in))
                        yield ' | '
                        yield str((undefined(name='acl_out') if l_1_acl_out is missing else l_1_acl_out))
                        yield ' |\n'
            l_1_ethernet_interface = l_1_port_channel_interface_name = l_1_port_channel_interface = l_1_description = l_1_channel_group = l_1_ip_address = l_1_vrf = l_1_mtu = l_1_shutdown = l_1_acl_in = l_1_acl_out = missing
        if (environment.getattr((undefined(name='port_channel_interface_ipv4') if l_0_port_channel_interface_ipv4 is missing else l_0_port_channel_interface_ipv4), 'configured') == True):
            pass
            yield '\n*Inherited from Port-Channel Interface\n'
        l_0_ip_nat_interfaces = (undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces)
        context.vars['ip_nat_interfaces'] = l_0_ip_nat_interfaces
        context.exported_vars.add('ip_nat_interfaces')
        template = environment.get_template('documentation/interfaces-ip-nat.j2', 'documentation/ethernet-interfaces.j2')
        gen = template.root_render_func(template.new_context(context.get_all(), True, {'encapsulation_dot1q_interfaces': l_0_encapsulation_dot1q_interfaces, 'err_cor_enc_intfs': l_0_err_cor_enc_intfs, 'ethernet_interface_ipv4': l_0_ethernet_interface_ipv4, 'ethernet_interface_ipv6': l_0_ethernet_interface_ipv6, 'ethernet_interface_pvlan': l_0_ethernet_interface_pvlan, 'ethernet_interface_vlan_xlate': l_0_ethernet_interface_vlan_xlate, 'ethernet_interfaces_isis': l_0_ethernet_interfaces_isis, 'ethernet_interfaces_vrrp_details': l_0_ethernet_interfaces_vrrp_details, 'evpn_dfe_ethernet_interfaces': l_0_evpn_dfe_ethernet_interfaces, 'evpn_es_ethernet_interfaces': l_0_evpn_es_ethernet_interfaces, 'evpn_mpls_ethernet_interfaces': l_0_evpn_mpls_ethernet_interfaces, 'flexencap_interfaces': l_0_flexencap_interfaces, 'ip_nat_interfaces': l_0_ip_nat_interfaces, 'link_tracking_interfaces': l_0_link_tracking_interfaces, 'multicast_interfaces': l_0_multicast_interfaces, 'phone_interfaces': l_0_phone_interfaces, 'port_channel_interface_ipv4': l_0_port_channel_interface_ipv4, 'port_channel_interface_ipv6': l_0_port_channel_interface_ipv6, 'port_channel_interfaces_isis': l_0_port_channel_interfaces_isis, 'priority_intfs': l_0_priority_intfs, 'sync_e_interfaces': l_0_sync_e_interfaces, 'tcp_mss_clampings': l_0_tcp_mss_clampings, 'te_interfaces': l_0_te_interfaces, 'transceiver_settings': l_0_transceiver_settings}))
        try:
            for event in gen:
                yield event
        finally: gen.close()
        l_0_ethernet_interface_ipv6 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['ethernet_interface_ipv6'] = l_0_ethernet_interface_ipv6
        context.exported_vars.add('ethernet_interface_ipv6')
        if not isinstance(l_0_ethernet_interface_ipv6, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_ethernet_interface_ipv6['configured'] = False
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (t_12(environment.getattr(l_1_ethernet_interface, 'ipv6_address')) or t_12(environment.getattr(l_1_ethernet_interface, 'ipv6_enable'), True)):
                pass
                if not isinstance(l_0_ethernet_interface_ipv6, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_ethernet_interface_ipv6['configured'] = True
                break
        l_1_ethernet_interface = missing
        l_0_port_channel_interface_ipv6 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_ipv6'] = l_0_port_channel_interface_ipv6
        context.exported_vars.add('port_channel_interface_ipv6')
        if not isinstance(l_0_port_channel_interface_ipv6, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_ipv6['configured'] = False
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (t_12(environment.getattr(l_1_port_channel_interface, 'ipv6_address')) or t_12(environment.getattr(l_1_port_channel_interface, 'ipv6_enable'), True)):
                pass
                if not isinstance(l_0_port_channel_interface_ipv6, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_ipv6['configured'] = True
                break
        l_1_port_channel_interface = missing
        if ((environment.getattr((undefined(name='ethernet_interface_ipv6') if l_0_ethernet_interface_ipv6 is missing else l_0_ethernet_interface_ipv6), 'configured') == True) or (environment.getattr((undefined(name='port_channel_interface_ipv6') if l_0_port_channel_interface_ipv6 is missing else l_0_port_channel_interface_ipv6), 'configured') == True)):
            pass
            yield '\n##### IPv6\n\n| Interface | Description | Channel Group | IPv6 Address | VRF | MTU | Shutdown | ND RA Disabled | Managed Config Flag | IPv6 ACL In | IPv6 ACL Out |\n| --------- | ----------- | --------------| ------------ | --- | --- | -------- | -------------- | -------------------| ----------- | ------------ |\n'
            for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
                l_1_port_channel_interface_name = resolve('port_channel_interface_name')
                l_1_port_channel_interface = resolve('port_channel_interface')
                l_1_description = resolve('description')
                l_1_channel_group = resolve('channel_group')
                l_1_ipv6_address = resolve('ipv6_address')
                l_1_vrf = resolve('vrf')
                l_1_mtu = resolve('mtu')
                l_1_shutdown = resolve('shutdown')
                l_1_nd_ra_disabled = resolve('nd_ra_disabled')
                l_1_managed_config_flag = resolve('managed_config_flag')
                l_1_ipv6_acl_in = resolve('ipv6_acl_in')
                l_1_ipv6_acl_out = resolve('ipv6_acl_out')
                _loop_vars = {}
                pass
                if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id')):
                    pass
                    l_1_port_channel_interface_name = str_join(('Port-Channel', environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), ))
                    _loop_vars['port_channel_interface_name'] = l_1_port_channel_interface_name
                    l_1_port_channel_interface = t_5(environment, t_11(context, t_1((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), []), 'name', 'arista.avd.defined', (undefined(name='port_channel_interface_name') if l_1_port_channel_interface_name is missing else l_1_port_channel_interface_name)))
                    _loop_vars['port_channel_interface'] = l_1_port_channel_interface
                    if (t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ipv6_address')) or t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ipv6_enable'), True)):
                        pass
                        l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                        _loop_vars['description'] = l_1_description
                        l_1_channel_group = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), '-')
                        _loop_vars['channel_group'] = l_1_channel_group
                        l_1_ipv6_address = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ipv6_address'), '-')
                        _loop_vars['ipv6_address'] = l_1_ipv6_address
                        l_1_vrf = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'vrf'), 'default')
                        _loop_vars['vrf'] = l_1_vrf
                        l_1_mtu = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'mtu'), '-')
                        _loop_vars['mtu'] = l_1_mtu
                        l_1_shutdown = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'shutdown'), '-')
                        _loop_vars['shutdown'] = l_1_shutdown
                        l_1_nd_ra_disabled = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ipv6_nd_ra_disabled'), '-')
                        _loop_vars['nd_ra_disabled'] = l_1_nd_ra_disabled
                        l_1_managed_config_flag = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ipv6_nd_managed_config_flag'), '-')
                        _loop_vars['managed_config_flag'] = l_1_managed_config_flag
                        l_1_ipv6_acl_in = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ipv6_access_group_in'), '-')
                        _loop_vars['ipv6_acl_in'] = l_1_ipv6_acl_in
                        l_1_ipv6_acl_out = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'ipv6_access_group_out'), '-')
                        _loop_vars['ipv6_acl_out'] = l_1_ipv6_acl_out
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                        yield ' | '
                        yield str((undefined(name='channel_group') if l_1_channel_group is missing else l_1_channel_group))
                        yield ' | *'
                        yield str((undefined(name='ipv6_address') if l_1_ipv6_address is missing else l_1_ipv6_address))
                        yield ' | *'
                        yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                        yield ' | *'
                        yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                        yield ' | *'
                        yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                        yield ' | *'
                        yield str((undefined(name='nd_ra_disabled') if l_1_nd_ra_disabled is missing else l_1_nd_ra_disabled))
                        yield ' | *'
                        yield str((undefined(name='managed_config_flag') if l_1_managed_config_flag is missing else l_1_managed_config_flag))
                        yield ' | *'
                        yield str((undefined(name='ipv6_acl_in') if l_1_ipv6_acl_in is missing else l_1_ipv6_acl_in))
                        yield ' | *'
                        yield str((undefined(name='ipv6_acl_out') if l_1_ipv6_acl_out is missing else l_1_ipv6_acl_out))
                        yield ' |\n'
                else:
                    pass
                    if (t_12(environment.getattr(l_1_ethernet_interface, 'ipv6_address')) or t_12(environment.getattr(l_1_ethernet_interface, 'ipv6_enable'), True)):
                        pass
                        l_1_description = t_1(environment.getattr(l_1_ethernet_interface, 'description'), '-')
                        _loop_vars['description'] = l_1_description
                        l_1_ipv6_address = t_1(environment.getattr(l_1_ethernet_interface, 'ipv6_address'), '-')
                        _loop_vars['ipv6_address'] = l_1_ipv6_address
                        l_1_vrf = t_1(environment.getattr(l_1_ethernet_interface, 'vrf'), 'default')
                        _loop_vars['vrf'] = l_1_vrf
                        l_1_mtu = t_1(environment.getattr(l_1_ethernet_interface, 'mtu'), '-')
                        _loop_vars['mtu'] = l_1_mtu
                        l_1_shutdown = t_1(environment.getattr(l_1_ethernet_interface, 'shutdown'), '-')
                        _loop_vars['shutdown'] = l_1_shutdown
                        l_1_nd_ra_disabled = t_1(environment.getattr(l_1_ethernet_interface, 'ipv6_nd_ra_disabled'), '-')
                        _loop_vars['nd_ra_disabled'] = l_1_nd_ra_disabled
                        l_1_managed_config_flag = t_1(environment.getattr(l_1_ethernet_interface, 'ipv6_nd_managed_config_flag'), '-')
                        _loop_vars['managed_config_flag'] = l_1_managed_config_flag
                        l_1_ipv6_acl_in = t_1(environment.getattr(l_1_ethernet_interface, 'ipv6_access_group_in'), '-')
                        _loop_vars['ipv6_acl_in'] = l_1_ipv6_acl_in
                        l_1_ipv6_acl_out = t_1(environment.getattr(l_1_ethernet_interface, 'ipv6_access_group_out'), '-')
                        _loop_vars['ipv6_acl_out'] = l_1_ipv6_acl_out
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                        yield ' | - | '
                        yield str((undefined(name='ipv6_address') if l_1_ipv6_address is missing else l_1_ipv6_address))
                        yield ' | '
                        yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                        yield ' | '
                        yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                        yield ' | '
                        yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                        yield ' | '
                        yield str((undefined(name='nd_ra_disabled') if l_1_nd_ra_disabled is missing else l_1_nd_ra_disabled))
                        yield ' | '
                        yield str((undefined(name='managed_config_flag') if l_1_managed_config_flag is missing else l_1_managed_config_flag))
                        yield ' | '
                        yield str((undefined(name='ipv6_acl_in') if l_1_ipv6_acl_in is missing else l_1_ipv6_acl_in))
                        yield ' | '
                        yield str((undefined(name='ipv6_acl_out') if l_1_ipv6_acl_out is missing else l_1_ipv6_acl_out))
                        yield ' |\n'
            l_1_ethernet_interface = l_1_port_channel_interface_name = l_1_port_channel_interface = l_1_description = l_1_channel_group = l_1_ipv6_address = l_1_vrf = l_1_mtu = l_1_shutdown = l_1_nd_ra_disabled = l_1_managed_config_flag = l_1_ipv6_acl_in = l_1_ipv6_acl_out = missing
        if (environment.getattr((undefined(name='port_channel_interface_ipv6') if l_0_port_channel_interface_ipv6 is missing else l_0_port_channel_interface_ipv6), 'configured') == True):
            pass
            yield '\n*Inherited from Port-Channel Interface\n'
        l_0_ethernet_interfaces_isis = []
        context.vars['ethernet_interfaces_isis'] = l_0_ethernet_interfaces_isis
        context.exported_vars.add('ethernet_interfaces_isis')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if ((((((((((t_12(environment.getattr(l_1_ethernet_interface, 'isis_enable')) or t_12(environment.getattr(l_1_ethernet_interface, 'isis_bfd'))) or t_12(environment.getattr(l_1_ethernet_interface, 'isis_metric'))) or t_12(environment.getattr(l_1_ethernet_interface, 'isis_circuit_type'))) or t_12(environment.getattr(l_1_ethernet_interface, 'isis_network_point_to_point'))) or t_12(environment.getattr(l_1_ethernet_interface, 'isis_passive'))) or t_12(environment.getattr(l_1_ethernet_interface, 'isis_hello_padding'))) or t_12(environment.getattr(l_1_ethernet_interface, 'isis_authentication_mode'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode'))):
                pass
                context.call(environment.getattr((undefined(name='ethernet_interfaces_isis') if l_0_ethernet_interfaces_isis is missing else l_0_ethernet_interfaces_isis), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        l_0_port_channel_interfaces_isis = []
        context.vars['port_channel_interfaces_isis'] = l_0_port_channel_interfaces_isis
        context.exported_vars.add('port_channel_interfaces_isis')
        for l_1_port_channel_interface in t_3((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if ((((((((((t_12(environment.getattr(l_1_port_channel_interface, 'isis_enable')) or t_12(environment.getattr(l_1_port_channel_interface, 'isis_bfd'))) or t_12(environment.getattr(l_1_port_channel_interface, 'isis_metric'))) or t_12(environment.getattr(l_1_port_channel_interface, 'isis_circuit_type'))) or t_12(environment.getattr(l_1_port_channel_interface, 'isis_network_point_to_point'))) or t_12(environment.getattr(l_1_port_channel_interface, 'isis_passive'))) or t_12(environment.getattr(l_1_port_channel_interface, 'isis_hello_padding'))) or t_12(environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'isis_authentication'), 'both'), 'mode'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'isis_authentication'), 'level_1'), 'mode'))) or t_12(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'isis_authentication'), 'level_2'), 'mode'))):
                pass
                context.call(environment.getattr((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        l_0_ethernet_interfaces_vrrp_details = []
        context.vars['ethernet_interfaces_vrrp_details'] = l_0_ethernet_interfaces_vrrp_details
        context.exported_vars.add('ethernet_interfaces_vrrp_details')
        for l_1_ethernet_interface in t_1((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), []):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'vrrp_ids')):
                pass
                context.call(environment.getattr((undefined(name='ethernet_interfaces_vrrp_details') if l_0_ethernet_interfaces_vrrp_details is missing else l_0_ethernet_interfaces_vrrp_details), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='ethernet_interfaces_vrrp_details') if l_0_ethernet_interfaces_vrrp_details is missing else l_0_ethernet_interfaces_vrrp_details)) > 0):
            pass
            yield '\n##### VRRP Details\n\n| Interface | VRRP-ID | Priority | Advertisement Interval | Preempt | Tracked Object Name(s) | Tracked Object Action(s) | IPv4 Virtual IP | IPv4 VRRP Version | IPv6 Virtual IP |\n| --------- | ------- | -------- | ---------------------- | --------| ---------------------- | ------------------------ | --------------- | ----------------- | --------------- |\n'
            for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces_vrrp_details') if l_0_ethernet_interfaces_vrrp_details is missing else l_0_ethernet_interfaces_vrrp_details), 'name'):
                _loop_vars = {}
                pass
                def t_13(fiter):
                    for l_2_vrid in fiter:
                        if t_12(environment.getattr(l_2_vrid, 'id')):
                            yield l_2_vrid
                for l_2_vrid in t_13(environment.getattr(l_1_ethernet_interface, 'vrrp_ids')):
                    l_2_row_tracked_object_name = resolve('row_tracked_object_name')
                    l_2_row_tracked_object_action = resolve('row_tracked_object_action')
                    l_2_row_id = l_2_row_prio_level = l_2_row_ad_interval = l_2_row_preempt = l_2_row_ipv4_virt = l_2_row_ipv4_vers = l_2_row_ipv6_virt = missing
                    _loop_vars = {}
                    pass
                    l_2_row_id = environment.getattr(l_2_vrid, 'id')
                    _loop_vars['row_id'] = l_2_row_id
                    l_2_row_prio_level = t_1(environment.getattr(l_2_vrid, 'priority_level'), '-')
                    _loop_vars['row_prio_level'] = l_2_row_prio_level
                    l_2_row_ad_interval = t_1(environment.getattr(environment.getattr(l_2_vrid, 'advertisement'), 'interval'), '-')
                    _loop_vars['row_ad_interval'] = l_2_row_ad_interval
                    l_2_row_preempt = 'Enabled'
                    _loop_vars['row_preempt'] = l_2_row_preempt
                    if t_12(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'enabled'), False):
                        pass
                        l_2_row_preempt = 'Disabled'
                        _loop_vars['row_preempt'] = l_2_row_preempt
                    if t_12(environment.getattr(l_2_vrid, 'tracked_object')):
                        pass
                        l_2_row_tracked_object_name = []
                        _loop_vars['row_tracked_object_name'] = l_2_row_tracked_object_name
                        l_2_row_tracked_object_action = []
                        _loop_vars['row_tracked_object_action'] = l_2_row_tracked_object_action
                        for l_3_tracked_obj in t_3(environment.getattr(l_2_vrid, 'tracked_object'), 'name'):
                            _loop_vars = {}
                            pass
                            context.call(environment.getattr((undefined(name='row_tracked_object_name') if l_2_row_tracked_object_name is missing else l_2_row_tracked_object_name), 'append'), environment.getattr(l_3_tracked_obj, 'name'), _loop_vars=_loop_vars)
                            if t_12(environment.getattr(l_3_tracked_obj, 'shutdown'), True):
                                pass
                                context.call(environment.getattr((undefined(name='row_tracked_object_action') if l_2_row_tracked_object_action is missing else l_2_row_tracked_object_action), 'append'), 'Shutdown', _loop_vars=_loop_vars)
                            elif t_12(environment.getattr(l_3_tracked_obj, 'decrement')):
                                pass
                                context.call(environment.getattr((undefined(name='row_tracked_object_action') if l_2_row_tracked_object_action is missing else l_2_row_tracked_object_action), 'append'), str_join(('Decrement ', environment.getattr(l_3_tracked_obj, 'decrement'), )), _loop_vars=_loop_vars)
                        l_3_tracked_obj = missing
                        l_2_row_tracked_object_name = t_8(context.eval_ctx, (undefined(name='row_tracked_object_name') if l_2_row_tracked_object_name is missing else l_2_row_tracked_object_name), ', ')
                        _loop_vars['row_tracked_object_name'] = l_2_row_tracked_object_name
                        l_2_row_tracked_object_action = t_8(context.eval_ctx, (undefined(name='row_tracked_object_action') if l_2_row_tracked_object_action is missing else l_2_row_tracked_object_action), ', ')
                        _loop_vars['row_tracked_object_action'] = l_2_row_tracked_object_action
                    l_2_row_ipv4_virt = t_1(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'address'), '-')
                    _loop_vars['row_ipv4_virt'] = l_2_row_ipv4_virt
                    l_2_row_ipv4_vers = t_1(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'version'), '2')
                    _loop_vars['row_ipv4_vers'] = l_2_row_ipv4_vers
                    l_2_row_ipv6_virt = t_1(environment.getattr(environment.getattr(l_2_vrid, 'ipv6'), 'address'), '-')
                    _loop_vars['row_ipv6_virt'] = l_2_row_ipv6_virt
                    yield '| '
                    yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='row_id') if l_2_row_id is missing else l_2_row_id))
                    yield ' | '
                    yield str((undefined(name='row_prio_level') if l_2_row_prio_level is missing else l_2_row_prio_level))
                    yield ' | '
                    yield str((undefined(name='row_ad_interval') if l_2_row_ad_interval is missing else l_2_row_ad_interval))
                    yield ' | '
                    yield str((undefined(name='row_preempt') if l_2_row_preempt is missing else l_2_row_preempt))
                    yield ' | '
                    yield str(t_1((undefined(name='row_tracked_object_name') if l_2_row_tracked_object_name is missing else l_2_row_tracked_object_name), '-'))
                    yield ' | '
                    yield str(t_1((undefined(name='row_tracked_object_action') if l_2_row_tracked_object_action is missing else l_2_row_tracked_object_action), '-'))
                    yield ' | '
                    yield str((undefined(name='row_ipv4_virt') if l_2_row_ipv4_virt is missing else l_2_row_ipv4_virt))
                    yield ' | '
                    yield str((undefined(name='row_ipv4_vers') if l_2_row_ipv4_vers is missing else l_2_row_ipv4_vers))
                    yield ' | '
                    yield str((undefined(name='row_ipv6_virt') if l_2_row_ipv6_virt is missing else l_2_row_ipv6_virt))
                    yield ' |\n'
                l_2_vrid = l_2_row_id = l_2_row_prio_level = l_2_row_ad_interval = l_2_row_preempt = l_2_row_tracked_object_name = l_2_row_tracked_object_action = l_2_row_ipv4_virt = l_2_row_ipv4_vers = l_2_row_ipv6_virt = missing
            l_1_ethernet_interface = missing
        if ((t_9((undefined(name='ethernet_interfaces_isis') if l_0_ethernet_interfaces_isis is missing else l_0_ethernet_interfaces_isis)) > 0) or (t_9((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis)) > 0)):
            pass
            yield '\n##### ISIS\n\n| Interface | Channel Group | ISIS Instance | ISIS BFD | ISIS Metric | Mode | ISIS Circuit Type | Hello Padding | ISIS Authentication Mode |\n| --------- | ------------- | ------------- | -------- | ----------- | ---- | ----------------- | ------------- | ------------------------ |\n'
            for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
                l_1_port_channel_interface_name = resolve('port_channel_interface_name')
                l_1_port_channel_interface = resolve('port_channel_interface')
                l_1_channel_group = resolve('channel_group')
                l_1_isis_instance = resolve('isis_instance')
                l_1_isis_bfd = resolve('isis_bfd')
                l_1_isis_metric = resolve('isis_metric')
                l_1_isis_circuit_type = resolve('isis_circuit_type')
                l_1_isis_hello_padding = resolve('isis_hello_padding')
                l_1_isis_authentication_mode = resolve('isis_authentication_mode')
                l_1_mode = resolve('mode')
                _loop_vars = {}
                pass
                if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id')):
                    pass
                    l_1_port_channel_interface_name = str_join(('Port-Channel', environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), ))
                    _loop_vars['port_channel_interface_name'] = l_1_port_channel_interface_name
                    l_1_port_channel_interface = t_5(environment, t_11(context, (undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis), 'name', 'arista.avd.defined', (undefined(name='port_channel_interface_name') if l_1_port_channel_interface_name is missing else l_1_port_channel_interface_name)))
                    _loop_vars['port_channel_interface'] = l_1_port_channel_interface
                    if t_12((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface)):
                        pass
                        l_1_channel_group = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), '-')
                        _loop_vars['channel_group'] = l_1_channel_group
                        l_1_isis_instance = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_enable'), '-')
                        _loop_vars['isis_instance'] = l_1_isis_instance
                        l_1_isis_bfd = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_bfd'), '-')
                        _loop_vars['isis_bfd'] = l_1_isis_bfd
                        l_1_isis_metric = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_metric'), '-')
                        _loop_vars['isis_metric'] = l_1_isis_metric
                        l_1_isis_circuit_type = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_circuit_type'), '-')
                        _loop_vars['isis_circuit_type'] = l_1_isis_circuit_type
                        l_1_isis_hello_padding = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_hello_padding'), '-')
                        _loop_vars['isis_hello_padding'] = l_1_isis_hello_padding
                        if t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'both'), 'mode')):
                            pass
                            l_1_isis_authentication_mode = environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'both'), 'mode')
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        elif (t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_1'), 'mode')) and t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_2'), 'mode'))):
                            pass
                            l_1_isis_authentication_mode = str_join(('Level-1: ', environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_1'), 'mode'), '<br>', 'Level-2: ', environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_2'), 'mode'), ))
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        elif t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_1'), 'mode')):
                            pass
                            l_1_isis_authentication_mode = str_join(('Level-1: ', environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_1'), 'mode'), ))
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        elif t_12(environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_2'), 'mode')):
                            pass
                            l_1_isis_authentication_mode = str_join(('Level-2: ', environment.getattr(environment.getattr(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication'), 'level_2'), 'mode'), ))
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        else:
                            pass
                            l_1_isis_authentication_mode = t_1(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_authentication_mode'), '-')
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        if t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_network_point_to_point'), True):
                            pass
                            l_1_mode = 'point-to-point'
                            _loop_vars['mode'] = l_1_mode
                        elif t_12(environment.getattr((undefined(name='port_channel_interface') if l_1_port_channel_interface is missing else l_1_port_channel_interface), 'isis_passive'), True):
                            pass
                            l_1_mode = 'passive'
                            _loop_vars['mode'] = l_1_mode
                        else:
                            pass
                            l_1_mode = '-'
                            _loop_vars['mode'] = l_1_mode
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='channel_group') if l_1_channel_group is missing else l_1_channel_group))
                        yield ' | *'
                        yield str((undefined(name='isis_instance') if l_1_isis_instance is missing else l_1_isis_instance))
                        yield ' | '
                        yield str((undefined(name='isis_bfd') if l_1_isis_bfd is missing else l_1_isis_bfd))
                        yield ' | *'
                        yield str((undefined(name='isis_metric') if l_1_isis_metric is missing else l_1_isis_metric))
                        yield ' | *'
                        yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                        yield ' | *'
                        yield str((undefined(name='isis_circuit_type') if l_1_isis_circuit_type is missing else l_1_isis_circuit_type))
                        yield ' | *'
                        yield str((undefined(name='isis_hello_padding') if l_1_isis_hello_padding is missing else l_1_isis_hello_padding))
                        yield ' | *'
                        yield str((undefined(name='isis_authentication_mode') if l_1_isis_authentication_mode is missing else l_1_isis_authentication_mode))
                        yield ' |\n'
                else:
                    pass
                    if (l_1_ethernet_interface in (undefined(name='ethernet_interfaces_isis') if l_0_ethernet_interfaces_isis is missing else l_0_ethernet_interfaces_isis)):
                        pass
                        l_1_channel_group = t_1(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'), '-')
                        _loop_vars['channel_group'] = l_1_channel_group
                        l_1_isis_instance = t_1(environment.getattr(l_1_ethernet_interface, 'isis_enable'), '-')
                        _loop_vars['isis_instance'] = l_1_isis_instance
                        l_1_isis_bfd = t_1(environment.getattr(l_1_ethernet_interface, 'isis_bfd'), '-')
                        _loop_vars['isis_bfd'] = l_1_isis_bfd
                        l_1_isis_metric = t_1(environment.getattr(l_1_ethernet_interface, 'isis_metric'), '-')
                        _loop_vars['isis_metric'] = l_1_isis_metric
                        l_1_isis_circuit_type = t_1(environment.getattr(l_1_ethernet_interface, 'isis_circuit_type'), '-')
                        _loop_vars['isis_circuit_type'] = l_1_isis_circuit_type
                        l_1_isis_hello_padding = t_1(environment.getattr(l_1_ethernet_interface, 'isis_hello_padding'), '-')
                        _loop_vars['isis_hello_padding'] = l_1_isis_hello_padding
                        if t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode')):
                            pass
                            l_1_isis_authentication_mode = environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode')
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        elif (t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode')) and t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode'))):
                            pass
                            l_1_isis_authentication_mode = str_join(('Level-1: ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode'), '<br>', 'Level-2: ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode'), ))
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        elif t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode')):
                            pass
                            l_1_isis_authentication_mode = str_join(('Level-1: ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode'), ))
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        elif t_12(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode')):
                            pass
                            l_1_isis_authentication_mode = str_join(('Level-2: ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode'), ))
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        else:
                            pass
                            l_1_isis_authentication_mode = t_1(environment.getattr(l_1_ethernet_interface, 'isis_authentication_mode'), '-')
                            _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                        if t_12(environment.getattr(l_1_ethernet_interface, 'isis_network_point_to_point'), True):
                            pass
                            l_1_mode = 'point-to-point'
                            _loop_vars['mode'] = l_1_mode
                        elif t_12(environment.getattr(l_1_ethernet_interface, 'isis_passive'), True):
                            pass
                            l_1_mode = 'passive'
                            _loop_vars['mode'] = l_1_mode
                        else:
                            pass
                            l_1_mode = '-'
                            _loop_vars['mode'] = l_1_mode
                        yield '| '
                        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                        yield ' | '
                        yield str((undefined(name='channel_group') if l_1_channel_group is missing else l_1_channel_group))
                        yield ' | '
                        yield str((undefined(name='isis_instance') if l_1_isis_instance is missing else l_1_isis_instance))
                        yield ' | '
                        yield str((undefined(name='isis_bfd') if l_1_isis_bfd is missing else l_1_isis_bfd))
                        yield ' | '
                        yield str((undefined(name='isis_metric') if l_1_isis_metric is missing else l_1_isis_metric))
                        yield ' | '
                        yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                        yield ' | '
                        yield str((undefined(name='isis_circuit_type') if l_1_isis_circuit_type is missing else l_1_isis_circuit_type))
                        yield ' | '
                        yield str((undefined(name='isis_hello_padding') if l_1_isis_hello_padding is missing else l_1_isis_hello_padding))
                        yield ' | '
                        yield str((undefined(name='isis_authentication_mode') if l_1_isis_authentication_mode is missing else l_1_isis_authentication_mode))
                        yield ' |\n'
            l_1_ethernet_interface = l_1_port_channel_interface_name = l_1_port_channel_interface = l_1_channel_group = l_1_isis_instance = l_1_isis_bfd = l_1_isis_metric = l_1_isis_circuit_type = l_1_isis_hello_padding = l_1_isis_authentication_mode = l_1_mode = missing
        if (t_9((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis)) > 0):
            pass
            yield '\n*Inherited from Port-Channel Interface\n'
        l_0_evpn_es_ethernet_interfaces = []
        context.vars['evpn_es_ethernet_interfaces'] = l_0_evpn_es_ethernet_interfaces
        context.exported_vars.add('evpn_es_ethernet_interfaces')
        l_0_evpn_dfe_ethernet_interfaces = []
        context.vars['evpn_dfe_ethernet_interfaces'] = l_0_evpn_dfe_ethernet_interfaces
        context.exported_vars.add('evpn_dfe_ethernet_interfaces')
        l_0_evpn_mpls_ethernet_interfaces = []
        context.vars['evpn_mpls_ethernet_interfaces'] = l_0_evpn_mpls_ethernet_interfaces
        context.exported_vars.add('evpn_mpls_ethernet_interfaces')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment')):
                pass
                context.call(environment.getattr((undefined(name='evpn_es_ethernet_interfaces') if l_0_evpn_es_ethernet_interfaces is missing else l_0_evpn_es_ethernet_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
                if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')):
                    pass
                    context.call(environment.getattr((undefined(name='evpn_dfe_ethernet_interfaces') if l_0_evpn_dfe_ethernet_interfaces is missing else l_0_evpn_dfe_ethernet_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
                if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'mpls')):
                    pass
                    context.call(environment.getattr((undefined(name='evpn_mpls_ethernet_interfaces') if l_0_evpn_mpls_ethernet_interfaces is missing else l_0_evpn_mpls_ethernet_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='evpn_es_ethernet_interfaces') if l_0_evpn_es_ethernet_interfaces is missing else l_0_evpn_es_ethernet_interfaces)) > 0):
            pass
            yield '\n##### EVPN Multihoming\n\n####### EVPN Multihoming Summary\n\n| Interface | Ethernet Segment Identifier | Multihoming Redundancy Mode | Route Target |\n| --------- | --------------------------- | --------------------------- | ------------ |\n'
            for l_1_evpn_es_ethernet_interface in (undefined(name='evpn_es_ethernet_interfaces') if l_0_evpn_es_ethernet_interfaces is missing else l_0_evpn_es_ethernet_interfaces):
                l_1_esi = l_1_redundancy = l_1_rt = missing
                _loop_vars = {}
                pass
                l_1_esi = t_1(environment.getattr(environment.getattr(l_1_evpn_es_ethernet_interface, 'evpn_ethernet_segment'), 'identifier'), '-')
                _loop_vars['esi'] = l_1_esi
                l_1_redundancy = t_1(environment.getattr(environment.getattr(l_1_evpn_es_ethernet_interface, 'evpn_ethernet_segment'), 'redundancy'), 'all-active')
                _loop_vars['redundancy'] = l_1_redundancy
                l_1_rt = t_1(environment.getattr(environment.getattr(l_1_evpn_es_ethernet_interface, 'evpn_ethernet_segment'), 'route_target'), '-')
                _loop_vars['rt'] = l_1_rt
                yield '| '
                yield str(environment.getattr(l_1_evpn_es_ethernet_interface, 'name'))
                yield ' | '
                yield str((undefined(name='esi') if l_1_esi is missing else l_1_esi))
                yield ' | '
                yield str((undefined(name='redundancy') if l_1_redundancy is missing else l_1_redundancy))
                yield ' | '
                yield str((undefined(name='rt') if l_1_rt is missing else l_1_rt))
                yield ' |\n'
            l_1_evpn_es_ethernet_interface = l_1_esi = l_1_redundancy = l_1_rt = missing
            if (t_9((undefined(name='evpn_dfe_ethernet_interfaces') if l_0_evpn_dfe_ethernet_interfaces is missing else l_0_evpn_dfe_ethernet_interfaces)) > 0):
                pass
                yield '\n####### Designated Forwarder Election Summary\n\n| Interface | Algorithm | Preference Value | Dont Preempt | Hold time | Subsequent Hold Time | Candidate Reachability Required |\n| --------- | --------- | ---------------- | ------------ | --------- | -------------------- | ------------------------------- |\n'
                for l_1_evpn_dfe_ethernet_interface in (undefined(name='evpn_dfe_ethernet_interfaces') if l_0_evpn_dfe_ethernet_interfaces is missing else l_0_evpn_dfe_ethernet_interfaces):
                    l_1_df_eth_settings = l_1_algorithm = l_1_pref_value = l_1_dont_preempt = l_1_hold_time = l_1_subsequent_hold_time = l_1_candidate_reachability = missing
                    _loop_vars = {}
                    pass
                    l_1_df_eth_settings = environment.getattr(environment.getattr(l_1_evpn_dfe_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')
                    _loop_vars['df_eth_settings'] = l_1_df_eth_settings
                    l_1_algorithm = t_1(environment.getattr((undefined(name='df_eth_settings') if l_1_df_eth_settings is missing else l_1_df_eth_settings), 'algorithm'), 'modulus')
                    _loop_vars['algorithm'] = l_1_algorithm
                    l_1_pref_value = t_1(environment.getattr((undefined(name='df_eth_settings') if l_1_df_eth_settings is missing else l_1_df_eth_settings), 'preference_value'), '-')
                    _loop_vars['pref_value'] = l_1_pref_value
                    l_1_dont_preempt = t_1(environment.getattr((undefined(name='df_eth_settings') if l_1_df_eth_settings is missing else l_1_df_eth_settings), 'dont_preempt'), False)
                    _loop_vars['dont_preempt'] = l_1_dont_preempt
                    l_1_hold_time = t_1(environment.getattr((undefined(name='df_eth_settings') if l_1_df_eth_settings is missing else l_1_df_eth_settings), 'hold_time'), '-')
                    _loop_vars['hold_time'] = l_1_hold_time
                    l_1_subsequent_hold_time = t_1(environment.getattr((undefined(name='df_eth_settings') if l_1_df_eth_settings is missing else l_1_df_eth_settings), 'subsequent_hold_time'), '-')
                    _loop_vars['subsequent_hold_time'] = l_1_subsequent_hold_time
                    l_1_candidate_reachability = t_1(environment.getattr((undefined(name='df_eth_settings') if l_1_df_eth_settings is missing else l_1_df_eth_settings), 'candidate_reachability_required'), False)
                    _loop_vars['candidate_reachability'] = l_1_candidate_reachability
                    yield '| '
                    yield str(environment.getattr(l_1_evpn_dfe_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='algorithm') if l_1_algorithm is missing else l_1_algorithm))
                    yield ' | '
                    yield str((undefined(name='pref_value') if l_1_pref_value is missing else l_1_pref_value))
                    yield ' | '
                    yield str((undefined(name='dont_preempt') if l_1_dont_preempt is missing else l_1_dont_preempt))
                    yield ' | '
                    yield str((undefined(name='hold_time') if l_1_hold_time is missing else l_1_hold_time))
                    yield ' | '
                    yield str((undefined(name='subsequent_hold_time') if l_1_subsequent_hold_time is missing else l_1_subsequent_hold_time))
                    yield ' | '
                    yield str((undefined(name='candidate_reachability') if l_1_candidate_reachability is missing else l_1_candidate_reachability))
                    yield ' |\n'
                l_1_evpn_dfe_ethernet_interface = l_1_df_eth_settings = l_1_algorithm = l_1_pref_value = l_1_dont_preempt = l_1_hold_time = l_1_subsequent_hold_time = l_1_candidate_reachability = missing
            if (t_9((undefined(name='evpn_mpls_ethernet_interfaces') if l_0_evpn_mpls_ethernet_interfaces is missing else l_0_evpn_mpls_ethernet_interfaces)) > 0):
                pass
                yield '\n####### EVPN-MPLS summary\n\n| Interface | Shared Index | Tunnel Flood Filter Time |\n| --------- | ------------ | ------------------------ |\n'
                for l_1_evpn_mpls_ethernet_interface in (undefined(name='evpn_mpls_ethernet_interfaces') if l_0_evpn_mpls_ethernet_interfaces is missing else l_0_evpn_mpls_ethernet_interfaces):
                    l_1_shared_index = l_1_tff_time = missing
                    _loop_vars = {}
                    pass
                    l_1_shared_index = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_evpn_mpls_ethernet_interface, 'evpn_ethernet_segment'), 'mpls'), 'shared_index'), '-')
                    _loop_vars['shared_index'] = l_1_shared_index
                    l_1_tff_time = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_evpn_mpls_ethernet_interface, 'evpn_ethernet_segment'), 'mpls'), 'tunnel_flood_filter_time'), '-')
                    _loop_vars['tff_time'] = l_1_tff_time
                    yield '| '
                    yield str(environment.getattr(l_1_evpn_mpls_ethernet_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='shared_index') if l_1_shared_index is missing else l_1_shared_index))
                    yield ' | '
                    yield str((undefined(name='tff_time') if l_1_tff_time is missing else l_1_tff_time))
                    yield ' |\n'
                l_1_evpn_mpls_ethernet_interface = l_1_shared_index = l_1_tff_time = missing
        l_0_err_cor_enc_intfs = []
        context.vars['err_cor_enc_intfs'] = l_0_err_cor_enc_intfs
        context.exported_vars.add('err_cor_enc_intfs')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding')):
                pass
                context.call(environment.getattr((undefined(name='err_cor_enc_intfs') if l_0_err_cor_enc_intfs is missing else l_0_err_cor_enc_intfs), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='err_cor_enc_intfs') if l_0_err_cor_enc_intfs is missing else l_0_err_cor_enc_intfs)) > 0):
            pass
            yield '\n##### Error Correction Encoding Interfaces\n\n| Interface | Enabled |\n| --------- | ------- |\n'
            for l_1_ethernet_interface in (undefined(name='err_cor_enc_intfs') if l_0_err_cor_enc_intfs is missing else l_0_err_cor_enc_intfs):
                l_1_enabled = resolve('enabled')
                _loop_vars = {}
                pass
                if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'enabled'), False):
                    pass
                    l_1_enabled = ['Disabled']
                    _loop_vars['enabled'] = l_1_enabled
                else:
                    pass
                    l_1_enabled = []
                    _loop_vars['enabled'] = l_1_enabled
                    if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'fire_code'), True):
                        pass
                        context.call(environment.getattr((undefined(name='enabled') if l_1_enabled is missing else l_1_enabled), 'append'), 'fire-code', _loop_vars=_loop_vars)
                    if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'reed_solomon'), True):
                        pass
                        context.call(environment.getattr((undefined(name='enabled') if l_1_enabled is missing else l_1_enabled), 'append'), 'reed-solomon', _loop_vars=_loop_vars)
                yield '| '
                yield str(environment.getattr(l_1_ethernet_interface, 'name'))
                yield ' | '
                yield str(t_8(context.eval_ctx, (undefined(name='enabled') if l_1_enabled is missing else l_1_enabled), '<br>'))
                yield ' |\n'
            l_1_ethernet_interface = l_1_enabled = missing
        l_0_priority_intfs = []
        context.vars['priority_intfs'] = l_0_priority_intfs
        context.exported_vars.add('priority_intfs')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'priority_flow_control'), 'enabled')):
                pass
                context.call(environment.getattr((undefined(name='priority_intfs') if l_0_priority_intfs is missing else l_0_priority_intfs), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='priority_intfs') if l_0_priority_intfs is missing else l_0_priority_intfs)) > 0):
            pass
            yield '\n#### Priority Flow Control\n\n| Interface | PFC | Priority | Drop/No_drop |\n'
            for l_1_priority_intf in (undefined(name='priority_intfs') if l_0_priority_intfs is missing else l_0_priority_intfs):
                _loop_vars = {}
                pass
                if t_12(environment.getattr(environment.getattr(l_1_priority_intf, 'priority_flow_control'), 'priorities')):
                    pass
                    for l_2_priority_block in t_3(environment.getattr(environment.getattr(l_1_priority_intf, 'priority_flow_control'), 'priorities')):
                        l_2_priority = l_2_drop_no_drop = missing
                        _loop_vars = {}
                        pass
                        l_2_priority = t_1(environment.getattr(l_2_priority_block, 'priority'), '-')
                        _loop_vars['priority'] = l_2_priority
                        l_2_drop_no_drop = t_1(environment.getattr(l_2_priority_block, 'no_drop'), '-')
                        _loop_vars['drop_no_drop'] = l_2_drop_no_drop
                        yield '| '
                        yield str(environment.getattr(l_1_priority_intf, 'name'))
                        yield ' | '
                        yield str(environment.getattr(environment.getattr(l_1_priority_intf, 'priority_flow_control'), 'enabled'))
                        yield ' | '
                        yield str((undefined(name='priority') if l_2_priority is missing else l_2_priority))
                        yield ' | '
                        yield str((undefined(name='drop_no_drop') if l_2_drop_no_drop is missing else l_2_drop_no_drop))
                        yield ' |\n'
                    l_2_priority_block = l_2_priority = l_2_drop_no_drop = missing
                else:
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_priority_intf, 'name'))
                    yield ' | '
                    yield str(environment.getattr(environment.getattr(l_1_priority_intf, 'priority_flow_control'), 'enabled'))
                    yield ' | - | - |\n'
            l_1_priority_intf = missing
        l_0_sync_e_interfaces = []
        context.vars['sync_e_interfaces'] = l_0_sync_e_interfaces
        context.exported_vars.add('sync_e_interfaces')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sync_e'), 'enable'), True):
                pass
                context.call(environment.getattr((undefined(name='sync_e_interfaces') if l_0_sync_e_interfaces is missing else l_0_sync_e_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='sync_e_interfaces') if l_0_sync_e_interfaces is missing else l_0_sync_e_interfaces)) > 0):
            pass
            yield '\n#### Synchronous Ethernet\n\n| Interface | Priority |\n| --------- | -------- |\n'
            for l_1_sync_e_interface in (undefined(name='sync_e_interfaces') if l_0_sync_e_interfaces is missing else l_0_sync_e_interfaces):
                _loop_vars = {}
                pass
                yield '| '
                yield str(environment.getattr(l_1_sync_e_interface, 'name'))
                yield ' | '
                yield str(t_1(environment.getattr(environment.getattr(l_1_sync_e_interface, 'sync_e'), 'priority'), '127'))
                yield ' |\n'
            l_1_sync_e_interface = missing
        l_0_te_interfaces = []
        context.vars['te_interfaces'] = l_0_te_interfaces
        context.exported_vars.add('te_interfaces')
        for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_12(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'enabled'), True):
                pass
                context.call(environment.getattr((undefined(name='te_interfaces') if l_0_te_interfaces is missing else l_0_te_interfaces), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
        l_1_ethernet_interface = missing
        if (t_9((undefined(name='te_interfaces') if l_0_te_interfaces is missing else l_0_te_interfaces)) > 0):
            pass
            yield '\n#### Traffic Engineering\n\n| Interface | Enabled | Administrative Groups | Metric | Max Reservable Bandwidth | Min-delay | SRLG |\n| --------- | ------- | --------------------- | ------ | ------------------------ | --------- | ---- |\n'
            for l_1_te_interface in (undefined(name='te_interfaces') if l_0_te_interfaces is missing else l_0_te_interfaces):
                l_1_te_bandwidth = resolve('te_bandwidth')
                l_1_te_min_del = resolve('te_min_del')
                l_1_admin_groups = l_1_te_enabled = l_1_te_srlg = l_1_te_metric = missing
                _loop_vars = {}
                pass
                l_1_admin_groups = t_8(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'administrative_groups'), ['-']), ',')
                _loop_vars['admin_groups'] = l_1_admin_groups
                l_1_te_enabled = t_1(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'enabled'), '-')
                _loop_vars['te_enabled'] = l_1_te_enabled
                l_1_te_srlg = t_1(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'srlg'), '-')
                _loop_vars['te_srlg'] = l_1_te_srlg
                l_1_te_metric = t_1(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'metric'), '-')
                _loop_vars['te_metric'] = l_1_te_metric
                if t_12(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'bandwidth')):
                    pass
                    l_1_te_bandwidth = str_join((environment.getattr(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'bandwidth'), 'number'), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'bandwidth'), 'unit'), ))
                    _loop_vars['te_bandwidth'] = l_1_te_bandwidth
                else:
                    pass
                    l_1_te_bandwidth = '-'
                    _loop_vars['te_bandwidth'] = l_1_te_bandwidth
                if t_12(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'min_delay_static')):
                    pass
                    l_1_te_min_del = str_join((environment.getattr(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'min_delay_static'), 'number'), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'min_delay_static'), 'unit'), ))
                    _loop_vars['te_min_del'] = l_1_te_min_del
                elif t_12(environment.getattr(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'min_delay_dynamic'), 'twamp_light_fallback')):
                    pass
                    l_1_te_min_del = str_join(('twamp-light, fallback ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'min_delay_dynamic'), 'twamp_light_fallback'), 'number'), ' ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_te_interface, 'traffic_engineering'), 'min_delay_dynamic'), 'twamp_light_fallback'), 'unit'), ))
                    _loop_vars['te_min_del'] = l_1_te_min_del
                else:
                    pass
                    l_1_te_min_del = '-'
                    _loop_vars['te_min_del'] = l_1_te_min_del
                yield '| '
                yield str(environment.getattr(l_1_te_interface, 'name'))
                yield ' | '
                yield str((undefined(name='te_enabled') if l_1_te_enabled is missing else l_1_te_enabled))
                yield ' | '
                yield str((undefined(name='admin_groups') if l_1_admin_groups is missing else l_1_admin_groups))
                yield ' | '
                yield str((undefined(name='te_metric') if l_1_te_metric is missing else l_1_te_metric))
                yield ' | '
                yield str((undefined(name='te_bandwidth') if l_1_te_bandwidth is missing else l_1_te_bandwidth))
                yield ' | '
                yield str((undefined(name='te_min_del') if l_1_te_min_del is missing else l_1_te_min_del))
                yield ' | '
                yield str((undefined(name='te_srlg') if l_1_te_srlg is missing else l_1_te_srlg))
                yield ' |\n'
            l_1_te_interface = l_1_admin_groups = l_1_te_enabled = l_1_te_srlg = l_1_te_metric = l_1_te_bandwidth = l_1_te_min_del = missing
        yield '\n#### Ethernet Interfaces Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/ethernet-interfaces.j2', 'documentation/ethernet-interfaces.j2')
        gen = template.root_render_func(template.new_context(context.get_all(), True, {'encapsulation_dot1q_interfaces': l_0_encapsulation_dot1q_interfaces, 'err_cor_enc_intfs': l_0_err_cor_enc_intfs, 'ethernet_interface_ipv4': l_0_ethernet_interface_ipv4, 'ethernet_interface_ipv6': l_0_ethernet_interface_ipv6, 'ethernet_interface_pvlan': l_0_ethernet_interface_pvlan, 'ethernet_interface_vlan_xlate': l_0_ethernet_interface_vlan_xlate, 'ethernet_interfaces_isis': l_0_ethernet_interfaces_isis, 'ethernet_interfaces_vrrp_details': l_0_ethernet_interfaces_vrrp_details, 'evpn_dfe_ethernet_interfaces': l_0_evpn_dfe_ethernet_interfaces, 'evpn_es_ethernet_interfaces': l_0_evpn_es_ethernet_interfaces, 'evpn_mpls_ethernet_interfaces': l_0_evpn_mpls_ethernet_interfaces, 'flexencap_interfaces': l_0_flexencap_interfaces, 'ip_nat_interfaces': l_0_ip_nat_interfaces, 'link_tracking_interfaces': l_0_link_tracking_interfaces, 'multicast_interfaces': l_0_multicast_interfaces, 'phone_interfaces': l_0_phone_interfaces, 'port_channel_interface_ipv4': l_0_port_channel_interface_ipv4, 'port_channel_interface_ipv6': l_0_port_channel_interface_ipv6, 'port_channel_interfaces_isis': l_0_port_channel_interfaces_isis, 'priority_intfs': l_0_priority_intfs, 'sync_e_interfaces': l_0_sync_e_interfaces, 'tcp_mss_clampings': l_0_tcp_mss_clampings, 'te_interfaces': l_0_te_interfaces, 'transceiver_settings': l_0_transceiver_settings}))
        try:
            for event in gen:
                yield event
        finally: gen.close()
        yield '```\n'

blocks = {}
debug_info = '7=110&17=113&18=124&19=126&20=128&25=130&33=132&34=134&35=136&37=138&38=140&39=142&41=143&42=145&44=146&45=148&47=152&50=154&51=156&53=160&55=162&56=164&57=167&59=181&60=183&61=185&62=187&63=189&64=191&66=195&68=197&69=199&70=202&75=218&83=220&84=222&85=224&87=226&88=228&89=230&91=231&92=233&94=234&95=236&96=238&97=240&100=242&101=244&103=248&105=250&106=253&108=265&109=267&110=269&111=271&112=273&113=275&115=279&117=281&118=284&125=298&126=301&127=304&128=307&129=309&130=310&131=312&132=313&133=315&134=317&135=318&136=320&140=322&146=325&147=329&148=331&149=333&150=335&151=338&154=349&160=352&161=364&162=366&163=368&166=370&167=372&168=374&169=376&170=378&173=380&174=382&175=384&176=386&177=388&179=390&182=392&183=394&184=396&185=398&186=400&189=402&190=404&191=406&192=408&193=410&195=413&199=440&200=445&201=446&202=449&206=453&207=454&210=456&216=459&217=463&218=465&219=467&220=470&225=477&226=482&227=483&228=486&230=490&231=491&234=493&240=496&241=499&242=501&243=505&245=518&246=522&248=535&249=540&250=542&251=544&253=548&255=551&257=564&258=566&259=570&260=572&261=575&268=585&269=588&270=591&271=593&274=595&280=598&281=604&282=606&283=608&285=610&286=612&288=615&292=624&293=627&294=630&295=632&298=634&304=637&305=642&306=644&307=646&308=648&309=650&312=654&314=656&315=659&319=666&320=669&321=672&322=674&325=676&331=679&332=682&333=685&334=688&337=695&338=698&343=705&344=708&345=711&346=713&349=715&355=718&356=722&357=724&358=726&359=728&360=731&364=742&365=745&366=748&367=750&370=752&376=755&377=760&378=762&379=764&380=766&384=770&386=773&388=779&389=781&390=783&391=785&395=789&397=792&402=799&403=804&404=805&405=808&406=812&407=813&410=815&411=820&412=821&413=824&414=828&415=829&418=831&424=834&425=847&426=849&427=851&430=853&431=855&432=857&433=859&434=861&435=863&436=865&437=867&438=869&439=872&442=892&443=894&444=896&445=898&446=900&447=902&448=904&449=906&450=909&455=926&460=929&461=932&463=938&464=943&465=944&466=947&467=951&468=952&471=954&472=959&473=960&474=963&475=967&476=968&479=970&485=973&486=988&487=990&488=992&491=994&492=996&493=998&494=1000&495=1002&496=1004&497=1006&498=1008&499=1010&500=1012&501=1014&502=1017&505=1041&506=1043&507=1045&508=1047&509=1049&510=1051&511=1053&512=1055&513=1057&514=1059&515=1062&520=1083&525=1086&526=1089&527=1092&538=1094&541=1096&542=1099&543=1102&554=1104&558=1106&559=1109&560=1112&561=1114&564=1116&570=1119&571=1122&572=1132&573=1134&574=1136&575=1138&576=1140&577=1142&579=1144&580=1146&581=1148&582=1150&583=1153&584=1154&585=1156&586=1157&587=1159&590=1161&591=1163&593=1165&594=1167&595=1169&596=1172&600=1194&606=1197&607=1210&608=1212&609=1214&611=1216&612=1218&613=1220&614=1222&615=1224&616=1226&617=1228&618=1230&619=1232&620=1234&621=1236&622=1238&623=1240&624=1242&625=1244&627=1248&629=1250&630=1252&631=1254&632=1256&634=1260&636=1263&639=1283&640=1285&641=1287&642=1289&643=1291&644=1293&645=1295&646=1297&647=1299&648=1301&649=1303&650=1305&651=1307&652=1309&653=1311&655=1315&657=1317&658=1319&659=1321&660=1323&662=1327&664=1330&669=1349&674=1352&675=1355&676=1358&677=1361&678=1364&679=1366&680=1367&681=1369&683=1370&684=1372&688=1374&696=1377&697=1381&698=1383&699=1385&700=1388&702=1397&708=1400&709=1404&710=1406&711=1408&712=1410&713=1412&714=1414&715=1416&716=1419&719=1434&725=1437&726=1441&727=1443&728=1446&732=1453&733=1456&734=1459&735=1461&738=1463&744=1466&745=1470&746=1472&748=1476&749=1478&750=1480&752=1481&753=1483&756=1485&759=1490&760=1493&761=1496&762=1498&765=1500&770=1503&771=1506&772=1508&773=1512&774=1514&775=1517&778=1529&782=1534&783=1537&784=1540&785=1542&788=1544&794=1547&795=1551&798=1556&799=1559&800=1562&801=1564&804=1566&810=1569&811=1575&812=1577&813=1579&814=1581&815=1583&816=1585&818=1589&820=1591&821=1593&822=1595&823=1597&825=1601&827=1604&834=1620'