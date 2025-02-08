from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/ip-name-server-groups.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ip_name_server_groups = resolve('ip_name_server_groups')
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
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='ip_name_server_groups') if l_0_ip_name_server_groups is missing else l_0_ip_name_server_groups)):
        pass
        yield '\n### IP Name Server Groups\n\n#### IP Name Server Groups Summary\n'
        for l_1_group in t_2((undefined(name='ip_name_server_groups') if l_0_ip_name_server_groups is missing else l_0_ip_name_server_groups), 'name'):
            _loop_vars = {}
            pass
            yield '\n##### '
            yield str(environment.getattr(l_1_group, 'name'))
            yield '\n'
            if t_3(environment.getattr(l_1_group, 'dns_domain')):
                pass
                yield '\nDNS Domain: '
                yield str(environment.getattr(l_1_group, 'dns_domain'))
                yield '\n'
            if t_3(environment.getattr(l_1_group, 'ip_domain_list')):
                pass
                yield '\nIP Domain List: '
                yield str(environment.getattr(l_1_group, 'ip_domain_list'))
                yield '\n'
            if t_3(environment.getattr(l_1_group, 'name_servers')):
                pass
                yield '\n| IP Address | VRF | Priority |\n| ---------- | --- | -------- |\n'
                for l_2_server in t_2(environment.getattr(l_1_group, 'name_servers'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_2_server, 'ip_address'))
                    yield ' | '
                    yield str(environment.getattr(l_2_server, 'vrf'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_2_server, 'priority'), '-'))
                    yield ' |\n'
                l_2_server = missing
        l_1_group = missing
        yield '\n#### IP Name Server Groups Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/ip-name-server-groups.j2', 'documentation/ip-name-server-groups.j2')
        gen = template.root_render_func(template.new_context(context.get_all(), True, {}))
        try:
            for event in gen:
                yield event
        finally: gen.close()
        yield '```\n'

blocks = {}
debug_info = '7=30&12=33&14=37&15=39&17=42&19=44&21=47&23=49&27=52&28=56&36=65'