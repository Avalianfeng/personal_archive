export interface Question {
  id: number;
  text: string;
  dimension: 'E' | 'I' | 'S' | 'N' | 'T' | 'F' | 'J' | 'P' | 'O' | 'C' | 'A' | 'N_BF' | 'EI_SA' | 'EI_SR' | 'EI_MO' | 'EI_EM' | 'EI_SS';
  direction: 1 | -1; // 1 for positive correlation with the trait, -1 for negative
}

export const questions: Question[] = [
  // MBTI: E/I (Extraversion vs Introversion)
  { id: 1, text: "I feel energized after spending time with a large group of people.", dimension: 'E', direction: 1 },
  { id: 2, text: "I prefer to process my thoughts internally before sharing them.", dimension: 'I', direction: 1 },
  { id: 3, text: "I am often the first to start a conversation with someone new.", dimension: 'E', direction: 1 },
  { id: 4, text: "I find solitary activities more rewarding than social ones.", dimension: 'I', direction: 1 },

  // MBTI: S/N (Sensing vs Intuition)
  { id: 5, text: "I focus more on the details of the present than on future possibilities.", dimension: 'S', direction: 1 },
  { id: 6, text: "I often look for the underlying meaning or patterns in events.", dimension: 'N', direction: 1 },
  { id: 7, text: "I prefer practical, hands-on tasks over theoretical discussions.", dimension: 'S', direction: 1 },
  { id: 8, text: "I am drawn to abstract concepts and complex systems.", dimension: 'N', direction: 1 },

  // MBTI: T/F (Thinking vs Feeling)
  { id: 9, text: "I rely on logic and objective analysis when making decisions.", dimension: 'T', direction: 1 },
  { id: 10, text: "I prioritize harmony and the feelings of others in my choices.", dimension: 'F', direction: 1 },
  { id: 11, text: "I value truth and accuracy more than social comfort.", dimension: 'T', direction: 1 },
  { id: 12, text: "I am deeply affected by the emotions of those around me.", dimension: 'F', direction: 1 },

  // MBTI: J/P (Judging vs Perceiving)
  { id: 13, text: "I prefer to have a clear plan and schedule for my day.", dimension: 'J', direction: 1 },
  { id: 14, text: "I enjoy keeping my options open and acting spontaneously.", dimension: 'P', direction: 1 },
  { id: 15, text: "I feel a sense of relief once a decision has been finalized.", dimension: 'J', direction: 1 },
  { id: 16, text: "I find strict deadlines to be more restrictive than helpful.", dimension: 'P', direction: 1 },

  // Big Five: Openness
  { id: 17, text: "I have a vivid imagination and enjoy creative pursuits.", dimension: 'O', direction: 1 },
  { id: 18, text: "I am interested in complex philosophical questions.", dimension: 'O', direction: 1 },
  { id: 19, text: "I prefer to stick to traditional ways of doing things.", dimension: 'O', direction: -1 },
  { id: 20, text: "I enjoy visiting art galleries or attending cultural events.", dimension: 'O', direction: 1 },

  // Big Five: Conscientiousness
  { id: 21, text: "I am always prepared and organized in my work.", dimension: 'C', direction: 1 },
  { id: 22, text: "I often leave things until the last minute.", dimension: 'C', direction: -1 },
  { id: 23, text: "I pay great attention to detail in everything I do.", dimension: 'C', direction: 1 },
  { id: 24, text: "I follow a strict routine to stay productive.", dimension: 'C', direction: 1 },

  // Big Five: Agreeableness
  { id: 25, text: "I am genuinely interested in other people's well-being.", dimension: 'A', direction: 1 },
  { id: 26, text: "I am quick to judge others for their mistakes.", dimension: 'A', direction: -1 },
  { id: 27, text: "I believe that most people are basically honest and good.", dimension: 'A', direction: 1 },
  { id: 28, text: "I often challenge others' opinions even if it causes tension.", dimension: 'A', direction: -1 },

  // Big Five: Neuroticism (Emotional Stability)
  { id: 29, text: "I often feel overwhelmed by stress or pressure.", dimension: 'N_BF', direction: 1 },
  { id: 30, text: "I am generally calm and relaxed, even in difficult situations.", dimension: 'N_BF', direction: -1 },
  { id: 31, text: "My mood changes frequently without a clear reason.", dimension: 'N_BF', direction: 1 },
  { id: 32, text: "I worry a lot about things that might go wrong.", dimension: 'N_BF', direction: 1 },

  // Emotional Intelligence: Self-Awareness
  { id: 33, text: "I can easily identify the specific emotion I am feeling at any moment.", dimension: 'EI_SA', direction: 1 },
  { id: 34, text: "I understand how my moods affect the people around me.", dimension: 'EI_SA', direction: 1 },
  { id: 35, text: "I am aware of my personal strengths and weaknesses.", dimension: 'EI_SA', direction: 1 },

  // Emotional Intelligence: Self-Regulation
  { id: 36, text: "I can stay focused and productive even when I am upset.", dimension: 'EI_SR', direction: 1 },
  { id: 37, text: "I think carefully before acting on my impulses.", dimension: 'EI_SR', direction: 1 },
  { id: 38, text: "I am able to recover quickly from setbacks or failures.", dimension: 'EI_SR', direction: 1 },

  // Emotional Intelligence: Empathy (formerly Social Awareness)
  { id: 39, text: "I can sense the 'vibe' or unspoken tension in a room.", dimension: 'EI_EM', direction: 1 },
  { id: 40, text: "I am good at seeing things from another person's perspective.", dimension: 'EI_EM', direction: 1 },
  { id: 41, text: "I notice subtle changes in people's body language or tone.", dimension: 'EI_EM', direction: 1 },

  // Emotional Intelligence: Social Skills (formerly Relationship Management)
  { id: 42, text: "I am effective at resolving conflicts between other people.", dimension: 'EI_SS', direction: 1 },
  { id: 43, text: "I find it easy to build rapport with new acquaintances.", dimension: 'EI_SS', direction: 1 },
  { id: 44, text: "I am good at motivating and inspiring others.", dimension: 'EI_SS', direction: 1 },

  // Emotional Intelligence: Motivation
  { id: 45, text: "I am driven to achieve my goals for my own personal satisfaction.", dimension: 'EI_MO', direction: 1 },
  { id: 46, text: "I remain optimistic even when I encounter significant obstacles.", dimension: 'EI_MO', direction: 1 },
  { id: 47, text: "I am always looking for ways to do things better or more efficiently.", dimension: 'EI_MO', direction: 1 },

  // Additional Mix to reach 60
  { id: 48, text: "I find it easy to stay objective during a heated debate.", dimension: 'T', direction: 1 },
  { id: 49, text: "I am often curious about why people act the way they do.", dimension: 'O', direction: 1 },
  { id: 50, text: "I keep my workspace very tidy and organized.", dimension: 'C', direction: 1 },
  { id: 51, text: "I tend to trust my 'gut feeling' more than hard data.", dimension: 'N', direction: 1 },
  { id: 52, text: "I am comfortable being the center of attention.", dimension: 'E', direction: 1 },
  { id: 53, text: "I find it difficult to say no to people's requests.", dimension: 'F', direction: 1 },
  { id: 54, text: "I like to explore new places without a set itinerary.", dimension: 'P', direction: 1 },
  { id: 55, text: "I rarely lose my temper, even when provoked.", dimension: 'N_BF', direction: -1 },
  { id: 56, text: "I am often the one who organizes social gatherings.", dimension: 'E', direction: 1 },
  { id: 57, text: "I value efficiency more than personal connection in a professional setting.", dimension: 'T', direction: 1 },
  { id: 58, text: "I am always looking for ways to improve existing systems.", dimension: 'N', direction: 1 },
  { id: 59, text: "I find it easy to adapt to unexpected changes in plans.", dimension: 'P', direction: 1 },
  { id: 60, text: "I am highly motivated by achieving my long-term goals.", dimension: 'C', direction: 1 }
];
