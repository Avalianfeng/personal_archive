// src/data/questions.js
export const questions = [
  {
    id: 1,
    question: "When you're at a party, what do you typically prefer to do?",
    options: [
      {
        text: "Meet new people and engage in multiple conversations throughout the night",
        value: "extraverted",
        dimensions: { EI: 3 },
      },
      {
        text: "Find one or two interesting people to have deeper conversations with",
        value: "introverted",
        dimensions: { EI: -3 },
      },
      {
        text: "Mix between both approaches depending on how I feel",
        value: "balanced",
        dimensions: { EI: 0 },
      },
    ],
  },
  {
    id: 2,
    question: "When making important decisions, what do you rely on most?",
    options: [
      {
        text: "Logical analysis and objective facts",
        value: "thinking",
        dimensions: { TF: 3 },
      },
      {
        text: "How it will affect people and what feels right",
        value: "feeling",
        dimensions: { TF: -3 },
      },
      {
        text: "A combination of logic and personal values",
        value: "balanced",
        dimensions: { TF: 0 },
      },
    ],
  },
  {
    id: 3,
    question: "How do you prefer to take in information?",
    options: [
      {
        text: "Focus on concrete facts and details that I can observe",
        value: "sensing",
        dimensions: { SN: 3 },
      },
      {
        text: "Look for patterns, meanings, and future possibilities",
        value: "intuitive",
        dimensions: { SN: -3 },
      },
      {
        text: "Use both approaches depending on the situation",
        value: "balanced",
        dimensions: { SN: 0 },
      },
    ],
  },
  {
    id: 4,
    question: "How do you approach your daily schedule?",
    options: [
      {
        text: "I like to plan ahead and stick to my schedule",
        value: "judging",
        dimensions: { JP: 3 },
      },
      {
        text: "I prefer to keep my options open and adapt as I go",
        value: "perceiving",
        dimensions: { JP: -3 },
      },
      {
        text: "I plan some things but stay flexible for spontaneous activities",
        value: "balanced",
        dimensions: { JP: 0 },
      },
    ],
  },
  {
    id: 5,
    question: "What energizes you most?",
    options: [
      {
        text: "Being around lots of people and social activities",
        value: "extraverted",
        dimensions: { EI: 2 },
      },
      {
        text: "Having quiet time alone to think and reflect",
        value: "introverted",
        dimensions: { EI: -2 },
      },
      {
        text: "A healthy balance of social time and alone time",
        value: "balanced",
        dimensions: { EI: 0 },
      },
    ],
  },
  {
    id: 6,
    question: "When working on a project, what's your natural approach?",
    options: [
      {
        text: "Start with concrete steps and work methodically through details",
        value: "sensing",
        dimensions: { SN: 2 },
      },
      {
        text: "Begin with the big picture and overall vision",
        value: "intuitive",
        dimensions: { SN: -2 },
      },
      {
        text: "Switch between detailed planning and big-picture thinking",
        value: "balanced",
        dimensions: { SN: 0 },
      },
    ],
  },
  {
    id: 7,
    question: "How do you typically handle conflict?",
    options: [
      {
        text: "Address it directly with logical arguments and objective analysis",
        value: "thinking",
        dimensions: { TF: 2 },
      },
      {
        text: "Try to understand everyone's feelings and find harmony",
        value: "feeling",
        dimensions: { TF: -2 },
      },
      {
        text: "Use both rational discussion and emotional understanding",
        value: "balanced",
        dimensions: { TF: 0 },
      },
    ],
  },
  {
    id: 8,
    question: "What describes your ideal work environment?",
    options: [
      {
        text: "Structured with clear deadlines and organized processes",
        value: "judging",
        dimensions: { JP: 2 },
      },
      {
        text: "Flexible with room for spontaneity and creative exploration",
        value: "perceiving",
        dimensions: { JP: -2 },
      },
      {
        text: "Some structure but with flexibility to adapt when needed",
        value: "balanced",
        dimensions: { JP: 0 },
      },
    ],
  },
];
