using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;

public class TriggerChest : MonoBehaviour {
    public Animator chest;
    public Animator nave;
    //public bool is_Open = false;
    bool firstTrigger = true;
    void Start()  { }

    void Update() {
        if(nave.GetAnimatorTransitionInfo(0).fullPathHash == 654500191) {
            nave.SetBool("is_Triggered", false);
        }
     }

    private void OnTriggerEnter(Collider other) {
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
