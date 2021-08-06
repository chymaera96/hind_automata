#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: aditya
"""

import music21
import numpy as np
import pickle
import random
import os
import sys
import uuid


def translate_notation(swaras):
  hindi = ['S',r'r','R','g','G','M','m','P','d','D','n','N']
  english = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
  trans =  dict(zip(hindi, english))
  note = []
  for s in swaras:
    if s!=',':
      octave = s[1]
      note.append(trans[s[0]]+octave)
    else:
      note.append(s)
  return note

def create_noteset():
  noteset = []
  hindi = ['S',r'r','R','g','G','M','m','P','d','D','n','N']
  for ix in range(3,6):
    for n in hindi:
      nt = n + str(ix)
      noteset.append(nt)
  noteset.append(',')
  return noteset

unotes = translate_notation(create_noteset())

with open(os.getcwd()+"/automata/bhupali.aut", "rb") as fp1:  
    bhupali_probs = pickle.load(fp1) 
    
with open(os.getcwd()+"/automata/yaman.aut", "rb") as fp2:  
    yaman_probs = pickle.load(fp2) 
    
with open(os.getcwd()+"/automata/bhairavi.aut", "rb") as fp3:  
    bhairavi_probs = pickle.load(fp3) 
    

    
def compute_fsm(gbr):
    s = np.sum(gbr) * 1.0
    w1 = gbr[0]/s
    w2 = gbr[1]/s
    w3 = gbr[2]/s
    p_transition_probs = w1*yaman_probs + w2*bhupali_probs + w3*bhairavi_probs
    print("Weighting parameters are as follows:\n")
    print("Yaman:"+str(w1))
    print("Bhupali:"+str(w2))
    print("Bhairavi:"+str(w3))
    piecewise_transition_probs = []
    ps = np.sum(p_transition_probs,1)
    ps[np.where(ps==0)] = .1
    p_transition_probs = np.transpose(np.transpose(p_transition_probs)/ps) 
    piecewise_transition_probs.append(p_transition_probs)
    
    # transition probabilities matrix between the unique notes in the piece
    transition_probs = np.zeros((len(unotes),len(unotes)))
    # computing generic transition_probs from piecewise_transition_probs
    for transition_prob in piecewise_transition_probs:
        transition_probs += transition_prob    
    GBR = np.array([w1,w2,w3])
    mw = np.argmax(GBR)
    # print(mw)
    return transition_probs, mw
    

def simulate(gbr):
    transition_probs,mw = compute_fsm(gbr)
    note_space_duration = 0.75
    num_beat_cycle = 25
    alankar_density = 2
    centre = int((len(unotes)-1)/3) 
    prev_swar_ind = centre  # Initialize the automata with the tonic in the middle octave
    taal = 16    # Number of beats in a beat cycle. Choosing 'teental'
    part = music21.stream.Part(id='flute')
    part.append(music21.instrument.Flute())
    prev_note = music21.note.Note(unotes[prev_swar_ind])
    backup_swar_ind = prev_swar_ind
    
    # Selecting the max weighted raga for alankars 
    yaman = ['S3','R3','G3','m3','P3','D3','N3','S4','R4','G4','m4','P4','D4','N4','S5','R5','G5','m5','P5','D5','N5',',']
    bhairavi = ['S3','r3','g3','M3','P3','d3','n3','S4','r4','g4','M4','P4','d4','n4','S5','r5','g5','M5','P5','d5','n5',',']
    bhupali = ['S3','R3','G3','P3','D3','S4','R4','G4','P4','D4','S5','R5','G5','P5','D5',',']
    mwraga = np.array([yaman,bhupali,bhairavi])
    R1_notes = translate_notation(mwraga[mw])
    for cycle in range(num_beat_cycle):
      notes_list = []
      measure = music21.stream.Measure(number=1)
      if cycle == 0:
        note = music21.note.Note(unotes[int((len(unotes)-1)/3)])
        note.duration.quarterLength = note_space_duration
        # print(note)
        measure.append(note)
      else:
        for taal_num in range(taal):
          while np.sum(transition_probs[prev_swar_ind,:]) < 1.0:
            # print('f')
            if prev_swar_ind > centre:
              prev_swar_ind -= 1
            else:
              prev_swar_ind += 1
          swar_ind = np.random.choice(np.arange(len(unotes)),p=transition_probs[prev_swar_ind,:])
    
          # Random seed for the alankar
          seed = random.uniform(-1, 1)
          if seed < 0 and taal_num != 0:
            notes_list[-1].duration.quarterLength = note_space_duration/alankar_density
    
            for ix in np.arange(note_space_duration/alankar_density,note_space_duration,note_space_duration/alankar_density):
              # print("aaaaaa")
              if unotes[swar_ind] == ',':
                notes_list[-1].duration.quarterLength += note_space_duration/alankar_density
              else:
                # insert a note with duration alankar_density
                this_note = music21.note.Note(unotes[swar_ind])
                this_note.duration.quarterLength = note_space_duration/alankar_density
                notes_list.append(this_note)
    
                # update previous swar to fill in next note in alankar
                prev_swar_ind = swar_ind
                prev_note = this_note
    
                while unotes[swar_ind] not in R1_notes:
                  if swar_ind > centre:
                    swar_ind -= 1
                  else:
                    swar_ind += 1
                alankar_ind = R1_notes.index(unotes[swar_ind])
                # get index for next note in alankar
                if seed < 0.5:
                  alankar_ind += 1
                else:
                  alankar_ind -= 1
    
                if alankar_ind > len(R1_notes): 
                  alankar_ind -= 2
                if alankar_ind < 0: 
                  alankar_ind += 2
                
                swar_ind = unotes.index(R1_notes[alankar_ind])
          
          else:
            if unotes[swar_ind] == ',' and taal_num==0:
              # print("Wrong starting note!")
              while unotes[swar_ind] == ',':
                  swar_ind = np.random.choice(np.arange(len(unotes)),p=transition_probs[backup_swar_ind,:])
    
          # extend note duration if current index denotes a ','
          if unotes[swar_ind] == ',':
            notes_list[-1].duration.quarterLength += note_space_duration
          else:
            # create a note object for one quarterLength
            this_note = music21.note.Note(unotes[swar_ind])
            this_note.duration.quarterLength = note_space_duration
    
            # add it to the list
            notes_list.append(this_note)
            # update note and swaram index for next iteration
            backup_swar_ind = prev_swar_ind
            prev_swar_ind = swar_ind
            prev_note = this_note
    
      for note in notes_list:
        # print(note)
        measure.append(note)
    
      # add measure to part
      part.append(measure)
    
    # create an empty score
    simulation = music21.stream.Score()
    # add the part to it
    simulation.append(part)
    filename = os.getcwd()+"/outputs/sim"+str(uuid.uuid4())+".mid"
    fp = simulation.write('midi', fp=filename)
    
    return filename
