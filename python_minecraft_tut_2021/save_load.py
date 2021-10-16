# Save and load file functions :D
def save():
    global subDic, megasets, subsets, subCubes, noise
    import pickle, os, sys
    # Create a new entity that combines all our
    # subsets and megasets, which we can
    # place onto a file.

    # First, let's open/create a file in the 
    # folder we are working in (working directory)
    # that we can save to.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('pickling.txt','wb') as f:
        e = Entity()
        for s in subsets:
            if s.enabled == True:
                s.parent = e
        for m in megasets:
            if m.enabled == True:
                m.parent = e
        e.combine(auto_destroy=False)
        terrainModel = [    e.model.vertices,
                            e.model.triangles,
                            e.model.colors,
                            e.model.uvs]
        buildsModel = [     varch.builds.model.vertices,
                            varch.builds.model.triangles,
                            varch.builds.model.colors,
                            varch.builds.model.uvs]
        # Set parents to default (scene).
        # And destroy our temporary terrain model.
        for s in subsets:
            s.parent = scene
        for m in megasets:
            m.parent = scene
        destroy(e)

        newlist = [ subject.position,
                    varch.tDic,
                    subDic,
                    terrainModel,
                    noise,
                    buildsModel,
                    sol4r.treeslist
                    ]
        
        # Write game state objects to file.
        pickle.dump(newlist, f)
        # Clear out temporary lists.
        newlist.clear()
        terrainModel.clear()

def load():
    import pickle, sys, os, copy as c
    global subDic, rad, theta, currentSubset
    global currentCube, currentMegaset, noise
    global canGenerate, generating

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open('pickling.txt', 'rb') as f:
        global subject, varch
        nd = pickle.load(f)

        # Populate our familiar terrain variables
        # with data from the saved file.

        subject.position = c.copy(nd[0])
        varch.tDic = c.copy(nd[1])
        subDic = c.copy(nd[2])
        tm = c.copy(nd[3])
        noise = c.copy(nd[4])
        bm = c.copy(nd[5])
        entslist = c.copy(nd[6]) # Trees :)

        # Now, let's delete all the current terrain.
        #  And builds!
        for s in subCubes:
            destroy(s)
        for s in subsets:
            destroy(s)
        for m in megasets:
            destroy(m)
        destroy(varch.builds)
        subCubes.clear()
        subsets.clear()
        megasets.clear()
        # Destroy all current trees in scene.
        sol4r.treesCounter = 0
        sol4r.treeslist.clear()
        sol4r.trees.combine()
        destroy(sol4r.trees)
        sol4r.trees=Entity()
        # Repopulate list of tree locations with
        # loaded data from file.
        sol4r.treeslist=entslist

        createTerrainEntities()
        # Reset terrain generation variables.

        # Go and plant loaded trees from list.
        for t in entslist:
            sol4r.plantTree(t[0],t[1],t[2])

        megasets[0] = Entity(model=Mesh(
                        vertices=tm[0],
                        triangles=tm[1],
                        colors=tm[2],
                        uvs=tm[3]),
                        texture=cubeTex)
        # Bug solved! Note the texture needs to 
        # be 'varch.buildTex' for the builds model,
        # not 'cubeTex'. The bug was caused by
        # shining the builds colours through the
        # terrain cube model.
        varch.builds = Entity(model=Mesh(
                        vertices=bm[0],
                        triangles=bm[1],
                        colors=bm[2],
                        uvs=bm[3]),
                        texture=varch.buildTex)

        # Reset gamestate.
        currentCube = 0
        currentMegaset = 2 # NB different.
        currentSubset = 0
        rad = 0
        theta = 0
        generating = -1
        canGenerate = -1