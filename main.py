def chooseRender():
    a=input("'3' to render 3d\n'2' to render 2d\n\n")
    if a.replace(' ', '') == "3":
        return 3
    elif a.replace(' ', '') == "2":
        return 2
    else:
        print("\nInvalid input\n")
        return chooseRender()

if chooseRender() == 3:
    import render3d
else:
    import render2d