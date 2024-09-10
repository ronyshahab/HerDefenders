
def precedence(sym:str)->int:

    preced={
        "+":2,
        "-":2,
        "*":3,
        "/":3,
        "(":0,
        ")":9
    }

    if sym not in preced:
        return 1

    return preced[sym]

def main():
    res=""
    userInput = str(input("Enter your infix string:"))
    userInput = userInput+"#"
    stack=[]
    top=None
    for i in userInput:
        if top==None:
            stack.append(i)
            top=precedence(i)
        elif precedence(i) >= top or i =="#" or precedence(i)>1:
            top=max(top, precedence(i))
            for j in range(len(stack)-1,-1,-1):
                if precedence(stack[j])==top or precedence(stack[j])==1 or i=="#" :
                    # print("I am called", stack[j], precedence(stack[j]), top)
                    if stack[j] not in["(",")"]:
                        res= res+ stack.pop(j)
            stack.append(i)
        elif precedence(i)< top :
            stack.append(i)
        print("This is ", i, stack, top, "=>", res)

    return res 
print(main())

# ab+cf*g/-
# ac/b*d+

