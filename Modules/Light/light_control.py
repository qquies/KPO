def toggle_light(state):
    if state == "on":
        return "Lights on"
    elif state == "off":
        return "Lights off"
    else:
        return "Unknown command!"

if __name__ == "__main__":
    print(toggle_light("on"))
    print(toggle_light("off"))
    print(toggle_light("test"))