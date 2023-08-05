import os


def get_fn(fn):
    this_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_path, 'data', fn)


repr_dict = {
    'c0': {
        '0': {
            'name': 'cartoon',
            'parameters': {
                'aspectRatio': 5,
                'assembly': 'default',
                'capped': True,
                'clipNear': 0,
                'colorDomain': '',
                'colorMode': 'hcl',
                'colorScale': 'RdYlBu',
                'colorScheme': 'atomindex',
                'colorValue': 9474192,
                'defaultAssembly': '',
                'diffuse': 16777215,
                'flatShaded': False,
                'lazy': False,
                'linewidth': 2,
                'metalness': 0,
                'opacity': 1,
                'radialSegments': 10,
                'radius': 'sstruc',
                'roughness': 0.4,
                'scale': 0.7,
                'sele': 'polymer',
                'side': 'double',
                'smoothSheet': False,
                'subdiv': 6,
                'tension': None,
                'visible': True,
                'wireframe': False
            }
        },
        '1': {
            'name': 'ball+stick',
            'parameters': {
                'aspectRatio': 2,
                'assembly': 'default',
                'bondSpacing': 0.85,
                'clipNear': 0,
                'colorDomain': '',
                'colorMode': 'hcl',
                'colorScale': '',
                'colorScheme': 'element',
                'colorValue': 9474192,
                'cylinderOnly': False,
                'defaultAssembly': '',
                'diffuse': 16777215,
                'disableImpostor': False,
                'flatShaded': False,
                'lazy': False,
                'lineOnly': False,
                'linewidth': 2,
                'metalness': 0,
                'multipleBond': False,
                'opacity': 1,
                'openEnded': True,
                'radialSegments': 10,
                'radius': 0.15,
                'roughness': 0.4,
                'scale': 1,
                'sele': 'hetero OR mol',
                'side': 'double',
                'sphereDetail': 1,
                'visible': True,
                'wireframe': False
            }
        },
        '2': {
            'name': 'ball+stick',
            'parameters': {
                'aspectRatio': 2,
                'assembly': 'default',
                'bondSpacing': 0.85,
                'clipNear': 0,
                'colorDomain': '',
                'colorMode': 'hcl',
                'colorScale': '',
                'colorScheme': 'element',
                'colorValue': 9474192,
                'cylinderOnly': False,
                'defaultAssembly': '',
                'diffuse': 16777215,
                'disableImpostor': False,
                'flatShaded': False,
                'lazy': False,
                'lineOnly': False,
                'linewidth': 2,
                'metalness': 0,
                'multipleBond': False,
                'opacity': 1,
                'openEnded': True,
                'radialSegments': 10,
                'radius': 0.15,
                'roughness': 0.4,
                'scale': 1,
                'sele': 'not protein and not nucleic',
                'side': 'double',
                'sphereDetail': 1,
                'visible': True,
                'wireframe': False
            }
        }
    }
}
