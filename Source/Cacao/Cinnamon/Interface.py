from Shared import * 

classes = pickle.load(open(picklepath, "rb"))

build_start = """
template<class D>
class ${cl} : public {cl}, public $CacBase {{
public:
    ~${cl}() {{
        endDestructor();
    }}
    ${cl}() {{}}
"""

build_body1 = """
    using r{id} = decltype(std::declval<{cl}>().{name}({defaults}));
    using c{id} = r{id}(${cl}::*)({params3}) {const};
    using d{id} = r{id}(D::*)({params3}) {const};
    r{id} {name}({params}) {const}{{
{function}
    }}
"""

build_body1_virtual = """
    using r{id} = decltype(std::declval<{cl}>().{name}({defaults}));
    using c{id} = r{id}(${cl}::*)({params3}) {const};
    using d{id} = r{id}(D::*)({params3}) {const};
    r{id} {name}({params}) {const}{{
{function}
    }}
"""

build_body1_static = """
    using r{id} = decltype(std::declval<{cl}>().{name}({defaults}));
    using c{id} = r{id}(*)({params3});
    using d{id} = r{id}(*)({params3});
    static r{id} {name}({params}) {const}{{
{function}
    }}
"""

# build_body1 = """
#     using c{id} = {type}({const}${cl}::*)({params3});
#     using d{id} = typename GetDerived<c{id}, D>::type;
#     using f{id} = typename GetStatic<c{id}>::type;
#     dupable {type} {name}({params}) {const}{{
#         {function}
#     }}
# """

# build_body1_virtual = """
#     using c{id} = {type}({const}${cl}::*)({params3});
#     using d{id} = typename GetDerived<c{id}, D>::type;
#     using f{id} = typename GetStatic<c{id}>::type;
#     dupable {type} {name}({params}) {const}{{
#         {function}
#     }}
# """

# build_body1_static = """
#     using c{id} = {type}(*)({params3});
#     using d{id} = {type}(*)({params3});
#     using f{id} = {type}(*)({params3});
#     dupable static {type} {name}({params}) {const}{{
#         {function}
#     }}
# """

build_body2_start = """
    static void apply() {{
        auto i = new D();
"""
    

build_body2_body = """
        if ((c{id}){{&${cl}::{name}}} != (d{id}){{&D::{name}}})
            m->registerHook(base+{offset}, FunctionScrapper::addressOfNonVirtual((d{id}){{&D::{name}}}));
"""

build_body2_body_static = """
        if ((c{id}){{&${cl}::{name}}} != (d{id}){{&D::{name}}})
            m->registerHook(base+{offset}, FunctionScrapper::addressOfNonVirtual((d{id}){{&D::{name}}}));
"""

build_body2_body_virtual = """
        if ((c{id}){{&${cl}::{name}}} != (d{id}){{&D::{name}}})
            m->registerHook(base+{offset}, FunctionScrapper::addressOfVirtual(i, (d{id}){{&D::{name}}}));
"""

build_body2_end = """
        // delete i;
    }\n"""
build_end = "};\n"

out = """// 
// Copyright camila314 & alk1m123 2021. 
// Autogenerated using a python script
//
#pragma once
#include <Base/InterfaceBase.hpp>
"""
for cl in classes:
    if "cocos2d" in cl.name:
        continue

    out += build_start.format(
        cl=cl.name,
    )

    for i, info in enumerate(cl.info):
        if not isinstance(info, CinnamonFunction) or info.declare.name[1:] in cl.name:
            continue
        body1 = build_body1
        if info.static:
            body1 = build_body1_static
        elif info.virtual:
            body1 = build_body1_virtual

        out += body1.format(
            name = info.declare.name,
            type = info.declare.type,
            cl = cl.name,
            offset = info.offset, 
            params = ', '.join(arg.getExpr(i) for i, arg in enumerate(info.parameters)),
            params2 = (', ' if not info.static and len(info.parameters) > 0 else "") + ', '.join(arg.getType(i) for i, arg in enumerate(info.parameters)),
            params3 = ', '.join(arg.getType(i) for i, arg in enumerate(info.parameters)),
            const = "const " if info.const else "",
            id = i,
            function = getFunctionImplementation(cl, info, i),
            defaults = ', '.join(f"std::declval<{arg.getType(i)}>()" for i, arg in enumerate(info.parameters)),
        )

    out += build_body2_start.format(cl=cl.name)

    for i, info in enumerate(cl.info):
        if not isinstance(info, CinnamonFunction) or info.declare.name[1:] in cl.name:
            continue
        body2 = build_body2_body
        if info.static:
            body2 = build_body2_body_static
        elif info.virtual:
            body2 = build_body2_body_virtual
        out += body2.format(
            name = info.declare.name,
            type = info.declare.type,
            cl = cl.name,
            offset = info.offset, 
            params = ', '.join(arg.getType(i) for i, arg in enumerate(info.parameters)),
            const = "const " if info.const else "",
            id = i,
        )

    out += build_body2_end
    out += build_end


with open(os.path.join(os.path.dirname(__file__), "..", "Interface.hpp"), "w") as f:
    f.write(out)
