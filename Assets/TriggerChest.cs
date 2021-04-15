using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TriggerChest : MonoBehaviour {
    public Animator chest;
    public Animator nave;
    //public bool is_Open = false;
    bool firstTrigger = true;
    void Start()  { }

    void Update() { }

    private void OnTriggerEnter(Collider other) {
        print("something");
        
        if(firstTrigger) {
            firstTrigger = false;
            chest.SetBool("first_Open", true);
        }
        else {
            if(!chest.GetBool("is_Open")) {
                chest.SetBool("is_Open", true); 
                nave.SetBool("is_Triggered", true);
            } else {
                chest.SetBool("is_Open", false); 
            }
        }
    }
}
