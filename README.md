# HM_ToolDev

Toolbox for Hypermesh Python API with custom Python tools.
As now, the available tools are:
  - CBEAM orientation tool - This tool orients CBEAM elements (selected by the user in HM GUI) and aligns them with the closest nodes from another user selection (selection by the user in HM GUI) and finds the closest reference node per element and aligns the element with that node. To be used, first the user MUST align all CBEAM with a reference node (can be any node), and only then use the tool to properly align the elements. After execution the user can delete the temporary alignment nodes to keep the CBEAM OFFT as BGG for example (not node dependent, but rather vector dependent).
