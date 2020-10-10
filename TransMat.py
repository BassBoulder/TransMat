import bpy
from contextlib import redirect_stdout

# Operator Code

class TransMatOperator(bpy.types.Operator):
    """Translates and Transfers Materials from Blender to Unreal"""
    bl_idname = "blui.transmat_operator"
    bl_label = "TransMat!"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):
        
        material = bpy.context.material
        nodes = material.node_tree.nodes
        gamecontentdirectory = "/Game/"
        exportdirectory = "D:\Blender\Scripts\TransmatOutputs\_"
        
        node_translate = {
        "ShaderNodeBsdfPrincipled":"unreal.MaterialExpressionMakeMaterialAttributes",
        "ShaderNodeMixShader":"unreal.MaterialExpressionBlendMaterialAttributes",
        "ShaderNodeAddShader":"unreal.MaterialExpressionAdd",
        "ShaderNodeInvert":"unreal.MaterialExpressionOneMinus",
        "ShaderNodeTexImage":"unreal.MaterialExpressionTextureSampleParameter2D",
        "ShaderNodeTexCoord":"unreal.MaterialExpressionTextureCoordinate",
        "ShaderNodeValue":"unreal.MaterialExpressionConstant",
        "ShaderNodeRGB":"unreal.MaterialExpressionConstant3Vector",
        # Math Node Operations
        "ADD":"unreal.MaterialExpressionAdd",
        "SUBTRACT":"unreal.MaterialExpressionSubtract",
        "MULTIPLY":"unreal.MaterialExpressionMultiply",
        "DIVIDE":"unreal.MaterialExpressionDivide",
        "SINE":"unreal.MaterialExpressionSine",
        "ARCSINE":"unreal.MaterialExpressionArcsine",
        "COSINE":"unreal.MaterialExpressionCosine",
        "ARCCOSINE":"unreal.MaterialExpressionArccossine",
        "POWER":"unreal.MaterialExpressionPower",
        "MINIMUM":"unreal.MaterialExpressionMin",
        "MAXIMUM":"unreal.MaterialExpressionMax",
        "ROUND":"unreal.MaterialExpressionRound",
        "ABSOLUTE":"unreal.MaterialExpressionAbs",
        # Mix RGB Blend Types
        "MIX":"unreal.MaterialExpressionLinearInterpolate"
        }
        
        
        # Exporting the material as a .py file to be run in Unreal
        with open(f'{exportdirectory}{material.name}_TM.py', 'w') as textoutput:

            with redirect_stdout(textoutput):
                # The file will contain all the print statements until execute
                # returns 'FINISHED'
                        
                print("import unreal")
                print("")
                print(f"{material.name}=unreal.AssetToolsHelpers.get_asset_tools().create_asset('{material.name}','{gamecontentdirectory}', unreal.Material, unreal.MaterialFactoryNew())")
                print(f"{material.name}.set_editor_property('use_material_attributes',True)")
                print("")
                print("create_expression = unreal.MaterialEditingLibrary.create_material_expression")
                print("")
                
                for node in nodes:

                    nodeinfo = {
                    "Blender Node": node.bl_idname,
                    "Unreal_Node": "",
                    "Node ID": node.name,
                    "Settings": {},
                    "Links": {}
                    }
                    
                    
                    # Value node contains a single float
                    if node.bl_idname == 'ShaderNodeValue':
#                        print(":::Settings::: ")
#                        print("Value: " + str(node.outputs[0].default_value))
                        
                        nodeinfo["Settings"] = {
                        "Value": node.outputs[0].default_value
                        }
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]}-400)")
                        
                        
                    # RGB node gives 4 float values for RGBA - alpha may be unnecessary
                    if node.bl_idname == "ShaderNodeRGB":
#                        print(":::Settings::: ")
#                        print("RGBA: (" + 
#                        str(round(node.outputs[0].default_value[0], 3)) + ",",
#                        str(round(node.outputs[0].default_value[1], 3)) + ",",
#                        str(round(node.outputs[0].default_value[2], 3)) + ",",
#                        str(round(node.outputs[0].default_value[3], 3)) + ")")
                        
                        nodeinfo["Settings"] = {
                        "R": round(node.outputs[0].default_value[0], 3),
                        "G": round(node.outputs[0].default_value[1], 3),
                        "B": round(node.outputs[0].default_value[2], 3),
                        }
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]                   
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]}-400)")
                        
                    # Math node retrieves the operation: ADD, MULTIPLY, COSINE, etc
                    if node.bl_idname == "ShaderNodeMath":
#                        print(":::Settings::: ")
#                        print(node.operation)
                        
                        nodeinfo["Settings"] = {"Operation":node.operation}
                        nodeinfo["Unreal_Node"] = node_translate[node.operation]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]}-400)")
                        
                    # Principled BSDF looks at inputs, rather than outputs
                    if node.bl_idname == "ShaderNodeBsdfPrincipled":
#                        print(":::Settings::: ")
#                        print("Base Color: (" + 
#                        str(round(node.inputs[0].default_value[0], 3)) + ",",
#                        str(round(node.inputs[0].default_value[1], 3)) + ",",
#                        str(round(node.inputs[0].default_value[2], 3)) + ",",
#                        str(round(node.inputs[0].default_value[3], 3)) + ")")
#                        print("Subsurface Color: (" + 
#                        str(round(node.inputs[3].default_value[0], 3)) + ",",
#                        str(round(node.inputs[3].default_value[1], 3)) + ",",
#                        str(round(node.inputs[3].default_value[2], 3)) + ",",
#                        str(round(node.inputs[3].default_value[3], 3)) + ")")
#                        print("Metallic: " + 
#                        str(node.inputs[4].default_value))
#                        print("Specular: " + 
#                        str(node.inputs[5].default_value))
#                        print("Roughness: " + 
#                        str(node.inputs[7].default_value))
#                        print("Emission: (" + 
#                        str(round(node.inputs[17].default_value[0], 3)) + ",",
#                        str(round(node.inputs[17].default_value[1], 3)) + ",",
#                        str(round(node.inputs[17].default_value[2], 3)) + ",",
#                        str(round(node.inputs[17].default_value[3], 3)) + ")")
#                        print("Alpha: " + 
#                        str(node.inputs[18].default_value))
#                        print("Normal: (" + 
#                        str(round(node.inputs[19].default_value[0], 3)) + ",",
#                        str(round(node.inputs[19].default_value[1], 3)) + ",",
#                        str(round(node.inputs[19].default_value[2], 3)) + ")")
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]-400})")
                    # Mix Shader
                    if node.bl_idname == "ShaderNodeMixRGB":
#                        print(node.name)
#                        print(node.blend_type)
                        
                        nodeinfo["Settings"] = {"Blend Type":node.blend_type}
                        nodeinfo["Unreal_Node"] = node_translate[node.blend_type]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]-400})")
                        
                    # Texture Coordinate
                    if node.bl_idname =="ShaderNodeTexCoord":
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]-400})")
                        
                    if node.bl_idname == "ShaderNodeTexImage":
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]-400})")
                        
                    if node.bl_idname == "ShaderNodeInvert":
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]-400})")
                        
                    if node.bl_idname == "ShaderNodeAddShader":
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]-400})")
                        
                    if node.bl_idname == "ShaderNodeMixShader":
                        nodeinfo["Unreal_Node"] = node_translate[node.bl_idname]
                        print(f"create_expression({material.name},{nodeinfo['Unreal_Node']},{node.location[0]-800},{node.location[1]-400})")
                        
                    #looping through the outputs
                    for output in node.outputs:
                        # only checking those that are connected
                        if output.is_linked:
                            # printing a nice, readable list of where the links start
                            # and end
                            for link in output.links:
                                nodeinfo["Links"] = {
                                "From node-" + link.from_node.name : "Socket-" + link.from_socket.name,
                                "To node-" + link.to_node.name : "Socket-" + link.to_socket.name
                                }  
        
        return {'FINISHED'}


# Panel UI

class TransMatPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the node editor"""
    bl_label = "TransMat"
    bl_idname = "BLUI_PT_transmat"
    bl_category = "TransMat"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Transfer Material!->", icon='MATERIAL')

        row = layout.row()
        row.operator("blui.transmat_operator")

# Register

def register():
    bpy.utils.register_class(TransMatPanel)
    bpy.utils.register_class(TransMatOperator)

def unregister():
    bpy.utils.unregister_class(TransMatPanel)
    bpy.utils.unregister_class(TransMatOperator)

if __name__ == "__main__":
    register()
