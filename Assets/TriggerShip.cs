using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TriggerShip : MonoBehaviour
{
    public bool animationFinished = false;
    public Animator animator;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(animationFinished) animator.SetBool("is_Triggered", false); 
    }
}
