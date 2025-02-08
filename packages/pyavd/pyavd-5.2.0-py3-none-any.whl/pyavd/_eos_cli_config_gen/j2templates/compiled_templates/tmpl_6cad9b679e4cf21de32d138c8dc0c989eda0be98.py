from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-path-selection.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_path_selection = resolve('router_path_selection')
    l_0_tcp_mss_ceiling_cli = resolve('tcp_mss_ceiling_cli')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['groupby']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'groupby' found.")
    try:
        t_4 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_5 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_5((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection)):
        pass
        yield '!\nrouter path-selection\n'
        if t_5(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'peer_dynamic_source')):
            pass
            yield '   peer dynamic source '
            yield str(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'peer_dynamic_source'))
            yield '\n'
        if t_5(environment.getattr(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'tcp_mss_ceiling'), 'ipv4_segment_size')):
            pass
            l_0_tcp_mss_ceiling_cli = 'tcp mss ceiling ipv4'
            context.vars['tcp_mss_ceiling_cli'] = l_0_tcp_mss_ceiling_cli
            context.exported_vars.add('tcp_mss_ceiling_cli')
            if (environment.getattr(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'tcp_mss_ceiling'), 'ipv4_segment_size') != 'auto'):
                pass
                l_0_tcp_mss_ceiling_cli = str_join(((undefined(name='tcp_mss_ceiling_cli') if l_0_tcp_mss_ceiling_cli is missing else l_0_tcp_mss_ceiling_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'tcp_mss_ceiling'), 'ipv4_segment_size'), ))
                context.vars['tcp_mss_ceiling_cli'] = l_0_tcp_mss_ceiling_cli
                context.exported_vars.add('tcp_mss_ceiling_cli')
            yield '   '
            yield str((undefined(name='tcp_mss_ceiling_cli') if l_0_tcp_mss_ceiling_cli is missing else l_0_tcp_mss_ceiling_cli))
            yield ' '
            yield str(t_1(environment.getattr(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'tcp_mss_ceiling'), 'direction'), 'ingress'))
            yield '\n'
        for l_1_interface_data in t_2(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'interfaces'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   interface '
            yield str(environment.getattr(l_1_interface_data, 'name'))
            yield '\n'
            if t_5(environment.getattr(environment.getattr(l_1_interface_data, 'metric_bandwidth'), 'transmit')):
                pass
                yield '      metric bandwidth transmit '
                yield str(environment.getattr(environment.getattr(l_1_interface_data, 'metric_bandwidth'), 'transmit'))
                yield ' Mbps\n'
            if t_5(environment.getattr(environment.getattr(l_1_interface_data, 'metric_bandwidth'), 'receive')):
                pass
                yield '      metric bandwidth receive '
                yield str(environment.getattr(environment.getattr(l_1_interface_data, 'metric_bandwidth'), 'receive'))
                yield ' Mbps\n'
        l_1_interface_data = missing
        for l_1_path_group in t_2(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'path_groups'), 'name'):
            l_1_path_group_def = missing
            _loop_vars = {}
            pass
            l_1_path_group_def = str_join(('path-group ', environment.getattr(l_1_path_group, 'name'), ))
            _loop_vars['path_group_def'] = l_1_path_group_def
            if t_5(environment.getattr(l_1_path_group, 'id')):
                pass
                l_1_path_group_def = str_join(((undefined(name='path_group_def') if l_1_path_group_def is missing else l_1_path_group_def), ' id ', environment.getattr(l_1_path_group, 'id'), ))
                _loop_vars['path_group_def'] = l_1_path_group_def
            yield '   !\n   '
            yield str((undefined(name='path_group_def') if l_1_path_group_def is missing else l_1_path_group_def))
            yield '\n'
            if t_5(environment.getattr(l_1_path_group, 'ipsec_profile')):
                pass
                yield '      ipsec profile '
                yield str(environment.getattr(l_1_path_group, 'ipsec_profile'))
                yield '\n'
            if t_5(environment.getattr(environment.getattr(l_1_path_group, 'keepalive'), 'auto'), True):
                pass
                yield '      keepalive interval auto\n'
            elif (t_5(environment.getattr(environment.getattr(l_1_path_group, 'keepalive'), 'interval')) and t_5(environment.getattr(environment.getattr(l_1_path_group, 'keepalive'), 'failure_threshold'))):
                pass
                yield '      keepalive interval '
                yield str(environment.getattr(environment.getattr(l_1_path_group, 'keepalive'), 'interval'))
                yield ' milliseconds failure-threshold '
                yield str(environment.getattr(environment.getattr(l_1_path_group, 'keepalive'), 'failure_threshold'))
                yield ' intervals\n'
            if t_5(environment.getattr(l_1_path_group, 'flow_assignment')):
                pass
                yield '      flow assignment '
                yield str(environment.getattr(l_1_path_group, 'flow_assignment'))
                yield '\n'
            for l_2_local_interface in t_2(environment.getattr(l_1_path_group, 'local_interfaces'), 'name'):
                l_2_local_interface_def = missing
                _loop_vars = {}
                pass
                l_2_local_interface_def = str_join(('local interface ', environment.getattr(l_2_local_interface, 'name'), ))
                _loop_vars['local_interface_def'] = l_2_local_interface_def
                if t_5(environment.getattr(l_2_local_interface, 'public_address')):
                    pass
                    l_2_local_interface_def = str_join(((undefined(name='local_interface_def') if l_2_local_interface_def is missing else l_2_local_interface_def), ' public address ', environment.getattr(l_2_local_interface, 'public_address'), ))
                    _loop_vars['local_interface_def'] = l_2_local_interface_def
                yield '      !\n      '
                yield str((undefined(name='local_interface_def') if l_2_local_interface_def is missing else l_2_local_interface_def))
                yield '\n'
                if t_5(environment.getattr(environment.getattr(l_2_local_interface, 'stun'), 'server_profiles')):
                    pass
                    yield '         stun server-profile '
                    yield str(t_4(context.eval_ctx, environment.getattr(environment.getattr(l_2_local_interface, 'stun'), 'server_profiles'), ' '))
                    yield '\n'
            l_2_local_interface = l_2_local_interface_def = missing
            for l_2_local_ip in t_2(environment.getattr(l_1_path_group, 'local_ips'), 'ip_address'):
                l_2_server_profiles = resolve('server_profiles')
                l_2_local_ip_def = missing
                _loop_vars = {}
                pass
                l_2_local_ip_def = str_join(('local ip ', environment.getattr(l_2_local_ip, 'ip_address'), ))
                _loop_vars['local_ip_def'] = l_2_local_ip_def
                if t_5(environment.getattr(l_2_local_ip, 'public_address')):
                    pass
                    l_2_local_ip_def = str_join(((undefined(name='local_ip_def') if l_2_local_ip_def is missing else l_2_local_ip_def), ' public address ', environment.getattr(l_2_local_ip, 'public_address'), ))
                    _loop_vars['local_ip_def'] = l_2_local_ip_def
                yield '      !\n      '
                yield str((undefined(name='local_ip_def') if l_2_local_ip_def is missing else l_2_local_ip_def))
                yield '\n'
                if t_5(environment.getattr(environment.getattr(l_2_local_ip, 'stun'), 'server_profiles')):
                    pass
                    l_2_server_profiles = t_2(environment.getattr(environment.getattr(l_2_local_ip, 'stun'), 'server_profiles'))
                    _loop_vars['server_profiles'] = l_2_server_profiles
                    yield '         stun server-profile '
                    yield str(t_4(context.eval_ctx, (undefined(name='server_profiles') if l_2_server_profiles is missing else l_2_server_profiles), ' '))
                    yield '\n'
            l_2_local_ip = l_2_local_ip_def = l_2_server_profiles = missing
            if t_5(environment.getattr(environment.getattr(l_1_path_group, 'dynamic_peers'), 'enabled'), True):
                pass
                yield '      !\n      peer dynamic\n'
                if t_5(environment.getattr(environment.getattr(l_1_path_group, 'dynamic_peers'), 'ip_local'), True):
                    pass
                    yield '         ip local\n'
                if t_5(environment.getattr(environment.getattr(l_1_path_group, 'dynamic_peers'), 'ipsec'), True):
                    pass
                    yield '         ipsec\n'
                elif t_5(environment.getattr(environment.getattr(l_1_path_group, 'dynamic_peers'), 'ipsec'), False):
                    pass
                    yield '         ipsec disabled\n'
            for l_2_static_peer in t_2(environment.getattr(l_1_path_group, 'static_peers'), 'router_ip'):
                _loop_vars = {}
                pass
                yield '      !\n      peer static router-ip '
                yield str(environment.getattr(l_2_static_peer, 'router_ip'))
                yield '\n'
                if t_5(environment.getattr(l_2_static_peer, 'name')):
                    pass
                    yield '         name '
                    yield str(environment.getattr(l_2_static_peer, 'name'))
                    yield '\n'
                for l_3_ipv4_address in t_1(environment.getattr(l_2_static_peer, 'ipv4_addresses'), []):
                    _loop_vars = {}
                    pass
                    yield '         ipv4 address '
                    yield str(l_3_ipv4_address)
                    yield '\n'
                l_3_ipv4_address = missing
            l_2_static_peer = missing
        l_1_path_group = l_1_path_group_def = missing
        for l_1_load_balance_policy in t_2(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'load_balance_policies'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   load-balance policy '
            yield str(environment.getattr(l_1_load_balance_policy, 'name'))
            yield '\n'
            if t_5(environment.getattr(l_1_load_balance_policy, 'latency')):
                pass
                yield '      latency '
                yield str(environment.getattr(l_1_load_balance_policy, 'latency'))
                yield '\n'
            if t_5(environment.getattr(l_1_load_balance_policy, 'jitter')):
                pass
                yield '      jitter '
                yield str(environment.getattr(l_1_load_balance_policy, 'jitter'))
                yield '\n'
            if t_5(environment.getattr(l_1_load_balance_policy, 'loss_rate')):
                pass
                yield '      loss-rate '
                yield str(environment.getattr(l_1_load_balance_policy, 'loss_rate'))
                yield '\n'
            if t_5(environment.getattr(l_1_load_balance_policy, 'lowest_hop_count'), True):
                pass
                yield '      hop count lowest\n'
            for (l_2_priority, l_2_entries) in t_3(environment, t_1(environment.getattr(l_1_load_balance_policy, 'path_groups'), []), 'priority', default=1):
                _loop_vars = {}
                pass
                for l_3_entry in t_2(l_2_entries, 'name'):
                    l_3_path_group_cli = missing
                    _loop_vars = {}
                    pass
                    l_3_path_group_cli = str_join(('path-group ', environment.getattr(l_3_entry, 'name'), ))
                    _loop_vars['path_group_cli'] = l_3_path_group_cli
                    if t_5(environment.getattr(l_3_entry, 'priority')):
                        pass
                        l_3_path_group_cli = str_join(((undefined(name='path_group_cli') if l_3_path_group_cli is missing else l_3_path_group_cli), ' priority ', environment.getattr(l_3_entry, 'priority'), ))
                        _loop_vars['path_group_cli'] = l_3_path_group_cli
                    yield '      '
                    yield str((undefined(name='path_group_cli') if l_3_path_group_cli is missing else l_3_path_group_cli))
                    yield '\n'
                l_3_entry = l_3_path_group_cli = missing
            l_2_priority = l_2_entries = missing
        l_1_load_balance_policy = missing
        l_1_loop = missing
        for l_1_policy, l_1_loop in LoopContext(t_2(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'policies'), 'name'), undefined):
            _loop_vars = {}
            pass
            yield '   !\n   policy '
            yield str(environment.getattr(l_1_policy, 'name'))
            yield '\n'
            if t_5(environment.getattr(l_1_policy, 'default_match')):
                pass
                yield '      default-match\n'
                if t_5(environment.getattr(environment.getattr(l_1_policy, 'default_match'), 'load_balance')):
                    pass
                    yield '         load-balance '
                    yield str(environment.getattr(environment.getattr(l_1_policy, 'default_match'), 'load_balance'))
                    yield '\n'
            l_2_loop = missing
            for l_2_rule, l_2_loop in LoopContext(t_2(environment.getattr(l_1_policy, 'rules'), 'id'), undefined):
                _loop_vars = {}
                pass
                if t_5(environment.getattr(l_2_rule, 'application_profile')):
                    pass
                    if (t_5(environment.getattr(l_1_policy, 'default_match')) or (not environment.getattr(l_2_loop, 'first'))):
                        pass
                        yield '      !\n'
                    yield '      '
                    yield str(environment.getattr(l_2_rule, 'id'))
                    yield ' application-profile '
                    yield str(environment.getattr(l_2_rule, 'application_profile'))
                    yield '\n'
                    if t_5(environment.getattr(l_2_rule, 'load_balance')):
                        pass
                        yield '         load-balance '
                        yield str(environment.getattr(l_2_rule, 'load_balance'))
                        yield '\n'
            l_2_loop = l_2_rule = missing
        l_1_loop = l_1_policy = missing
        for l_1_vrf in t_2(environment.getattr((undefined(name='router_path_selection') if l_0_router_path_selection is missing else l_0_router_path_selection), 'vrfs'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   vrf '
            yield str(environment.getattr(l_1_vrf, 'name'))
            yield '\n'
            if t_5(environment.getattr(l_1_vrf, 'path_selection_policy')):
                pass
                yield '      path-selection-policy '
                yield str(environment.getattr(l_1_vrf, 'path_selection_policy'))
                yield '\n'
        l_1_vrf = missing

blocks = {}
debug_info = '7=43&10=46&11=49&13=51&14=53&15=56&16=58&18=62&20=66&22=70&23=72&24=75&26=77&27=80&31=83&32=87&33=89&34=91&37=94&38=96&39=99&41=101&43=104&45=107&47=111&48=114&51=116&52=120&53=122&54=124&57=127&58=129&59=132&63=135&64=140&65=142&66=144&69=147&70=149&71=151&72=154&76=157&79=160&82=163&84=166&89=169&91=173&92=175&93=178&96=180&97=184&102=189&104=193&105=195&106=198&108=200&109=203&111=205&112=208&114=210&117=213&118=216&119=220&120=222&121=224&123=227&128=233&130=237&131=239&133=242&134=245&137=248&138=251&139=253&142=257&143=261&144=264&150=268&152=272&153=274&154=277'