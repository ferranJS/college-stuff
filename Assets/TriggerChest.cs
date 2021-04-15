using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TriggerChest : MonoBehaviour
{
   
    public Animator animator;
    public Animator nave;
    //public bool is_Open = false;
    bool firstTrigger = true;
    void Start()
    {
        //Get the Animator attached to the GameObject you are intending to animate.
       // m_Animator = gameObject.GetComponent<Animator>();
    }

    //Moves this GameObject 2 units a second in the forward direction
    void Update()
    {
        // if(Input.GetKeyDown(KeyCode.T)) 
        //     if(animator.GetBool("is_Open")) {
        //         animator.SetBool("is_Open", false); 
        //     } else {
        //         animator.SetBool("is_Open", true); 
        //         nave.SetBool("is_Triggered", true);
        //     }

    }

    //Upon collision with another GameObject, this GameObject will reverse direction
    private void OnTriggerEnter(Collider other)
    {
        print("something");
        
        if(firstTrigger) {
            firstTrigger = false;
            animator.SetBool("first_Open", true);
        }
        else {
            if(!animator.GetBool("is_Open")) {
                animator.SetBool("is_Open", true); 
                nave.SetBool("is_Triggered", true);
            } else {
                animator.SetBool("is_Open", false); 
            }
        }
    }
}
