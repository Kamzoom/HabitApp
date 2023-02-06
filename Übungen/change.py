import Input
print(Input.weeklyHabitlist)

def eraseHabit():
    print("Do you want to erase  an habit y or n")
    print("Witch habit do you want to erase? A weekly or a daily?")
    choose = input()
    print("This are your habits : ")
    if choose=="weekly":
        for object in Input.weeklyHabitlist:
            print(object.name)
        print("Witch habit do you want to erase?")
        toRemove=input()
        for object in Input.weeklyHabitlist:
            if(object.name==toRemove):
                Input.weeklyHabitlist.remove(object)
    elif choose=="daily":
        for object in Input.dailyHabitlist:
            print(object.name)
        print("Witch habit do you want to erase?")
        toRemove=input()
        for object in Input.dailyHabitlist:
            if(object.name==toRemove):
                Input.dailyHabitlist.remove(object)




print((Input.weeklyHabitlist))
