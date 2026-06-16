/* ============================================================
   PERSONA — MBTI Profiler
   Modular vanilla-JS application
   ============================================================ */
(function () {
  'use strict';
  const MBTI = (window.MBTI = {});

  /* =============================================================
     DATA: dimensions, questions, types, compatibility
     ============================================================= */
  MBTI.Data = {
    dimensions: [
      { code: 'EI', a: 'E', b: 'I', aName: 'Extraversion', bName: 'Introversion',
        desc: 'Where you draw energy: from people and action (E) or solitude and reflection (I).' },
      { code: 'SN', a: 'N', b: 'S', aName: 'Intuition', bName: 'Sensing',
        desc: 'How you take in information: through patterns & possibilities (N) or facts & details (S).' },
      { code: 'TF', a: 'T', b: 'F', aName: 'Thinking', bName: 'Feeling',
        desc: 'How you decide: through logic & consistency (T) or values & harmony (F).' },
      { code: 'JP', a: 'J', b: 'P', aName: 'Judging', bName: 'Perceiving',
        desc: 'How you live: planned & decisive (J) or spontaneous & adaptable (P).' }
    ],

    // 60 questions — 15 per dimension. direction +1 means SA pushes toward dim.a (E/N/T/J), -1 toward dim.b
    questions: [
      // E vs I (a=E, b=I)
      { t: 'I feel energized after spending time with a group of people.', d: 'EI', dir: +1 },
      { t: 'I prefer quiet evenings alone over busy social events.', d: 'EI', dir: -1 },
      { t: 'I think out loud and process ideas through conversation.', d: 'EI', dir: +1 },
      { t: 'I need significant alone time to recharge.', d: 'EI', dir: -1 },
      { t: 'I find it easy to start conversations with strangers.', d: 'EI', dir: +1 },
      { t: 'I get drained by extended social interaction.', d: 'EI', dir: -1 },
      { t: 'In meetings, I tend to speak up early.', d: 'EI', dir: +1 },
      { t: 'I usually listen more than I talk.', d: 'EI', dir: -1 },
      { t: 'I enjoy being the centre of attention.', d: 'EI', dir: +1 },
      { t: 'I prefer a small circle of close friends to many acquaintances.', d: 'EI', dir: -1 },
      { t: 'I think best when I can talk through a problem with others.', d: 'EI', dir: +1 },
      { t: 'I prefer to think a question through privately before answering.', d: 'EI', dir: -1 },
      { t: 'I am drawn to roles that involve frequent interaction.', d: 'EI', dir: +1 },
      { t: 'I find deep one-on-one conversation more rewarding than mingling.', d: 'EI', dir: -1 },
      { t: 'I can comfortably introduce myself to a room of strangers.', d: 'EI', dir: +1 },

      // S vs N (a=N, b=S)
      { t: 'I am drawn to abstract theories and big-picture ideas.', d: 'SN', dir: +1 },
      { t: 'I trust concrete facts more than hunches.', d: 'SN', dir: -1 },
      { t: 'I notice patterns and connections others miss.', d: 'SN', dir: +1 },
      { t: 'I focus on what is real and present, not speculation.', d: 'SN', dir: -1 },
      { t: 'I enjoy imagining future possibilities.', d: 'SN', dir: +1 },
      { t: 'I prefer step-by-step practical instructions.', d: 'SN', dir: -1 },
      { t: 'Metaphors and symbolism come easily to me.', d: 'SN', dir: +1 },
      { t: 'I value tradition and proven methods.', d: 'SN', dir: -1 },
      { t: 'I often think about what could be rather than what is.', d: 'SN', dir: +1 },
      { t: 'I rely on my five senses and direct experience.', d: 'SN', dir: -1 },
      { t: 'New theoretical concepts excite me.', d: 'SN', dir: +1 },
      { t: 'I prefer hands-on, tangible work.', d: 'SN', dir: -1 },
      { t: 'I see ideas as starting points to be explored.', d: 'SN', dir: +1 },
      { t: 'I notice small details others overlook.', d: 'SN', dir: -1 },
      { t: 'I am more interested in innovation than in tradition.', d: 'SN', dir: +1 },

      // T vs F (a=T, b=F)
      { t: 'I make decisions based on logic, even when emotions are at stake.', d: 'TF', dir: +1 },
      { t: 'I weigh how a decision will affect people emotionally before acting.', d: 'TF', dir: -1 },
      { t: 'I value fairness and consistency over harmony.', d: 'TF', dir: +1 },
      { t: 'I value harmony in relationships above being right.', d: 'TF', dir: -1 },
      { t: 'I can give critical feedback without much hesitation.', d: 'TF', dir: +1 },
      { t: 'I find it difficult to deliver criticism that may hurt someone.', d: 'TF', dir: -1 },
      { t: 'I tend to step back and analyse before reacting emotionally.', d: 'TF', dir: +1 },
      { t: 'I trust my emotional response as a guide.', d: 'TF', dir: -1 },
      { t: 'I value truth more than tact.', d: 'TF', dir: +1 },
      { t: 'I value tact more than blunt truth.', d: 'TF', dir: -1 },
      { t: 'I tend to detach from a problem to think clearly.', d: 'TF', dir: +1 },
      { t: 'I empathise easily with people in distress.', d: 'TF', dir: -1 },
      { t: 'Justice matters more to me than mercy.', d: 'TF', dir: +1 },
      { t: 'Mercy matters more to me than rigid justice.', d: 'TF', dir: -1 },
      { t: 'I rely on objective criteria when judging a situation.', d: 'TF', dir: +1 },

      // J vs P (a=J, b=P)
      { t: 'I make plans and stick to them.', d: 'JP', dir: +1 },
      { t: 'I prefer to keep my options open.', d: 'JP', dir: -1 },
      { t: 'I like having clear deadlines and structure.', d: 'JP', dir: +1 },
      { t: 'I work best in spurts, near deadlines.', d: 'JP', dir: -1 },
      { t: 'I feel uneasy when things are unresolved.', d: 'JP', dir: +1 },
      { t: 'I am energised by spontaneity and last-minute changes.', d: 'JP', dir: -1 },
      { t: 'I make to-do lists and check them off.', d: 'JP', dir: +1 },
      { t: 'I prefer to go with the flow of the day.', d: 'JP', dir: -1 },
      { t: 'I like decisions to be settled quickly.', d: 'JP', dir: +1 },
      { t: 'I delay decisions to gather more information.', d: 'JP', dir: -1 },
      { t: 'I prefer a tidy, organised workspace.', d: 'JP', dir: +1 },
      { t: 'My workspace tends to be a creative jumble.', d: 'JP', dir: -1 },
      { t: 'I feel satisfied when a project closes neatly.', d: 'JP', dir: +1 },
      { t: 'I enjoy juggling several projects at once.', d: 'JP', dir: -1 },
      { t: 'Routine and predictability comfort me.', d: 'JP', dir: +1 }
    ],

    types: {
      INTJ: {
        nickname: 'The Architect', icon: '♛', color: 'linear-gradient(135deg, #7c3aed, #4338ca)',
        group: 'Analyst',
        overview: 'Strategic, independent thinkers driven by long-range vision. INTJs see the chess game several moves ahead and engineer plans to get there.',
        strengths: ['Strategic foresight', 'Independent problem-solving', 'High standards', 'Decisive under pressure', 'Pattern recognition'],
        weaknesses: ['Can seem aloof', 'Impatient with inefficiency', 'Dismissive of intuition-free arguments', 'Perfectionism', 'Reluctant to share half-formed ideas'],
        communication: 'Direct, precise, and idea-driven. Prefers written or one-on-one over small talk. Asks pointed questions to test logic.',
        leadership: 'Visionary leader who sets ambitious targets and trusts capable people to execute. Leads through architecture, not charisma.',
        learning: 'Self-directed and conceptual. Learns by building mental models — needs the "why" before the "how".',
        workplace: 'Thrives in autonomous, intellectually challenging roles. Frustrated by busywork and inefficient process.',
        careers: ['Strategy consultant', 'Software architect', 'Research scientist', 'Investment analyst', 'Systems engineer'],
        teamwork: 'Best as the strategist on a team — give them the long-term play and let others handle execution and morale.',
        stress: 'Under stress, becomes overly critical, withdrawn, and obsessed with details that normally would not bother them.',
        growth: ['Practice expressing emotions openly', 'Listen to instinctive responses without dissecting them', 'Acknowledge effort, not just results'],
        famous: ['Elon Musk', 'Michelle Obama', 'Friedrich Nietzsche', 'Mark Zuckerberg'],
        relationships: 'Loyal but selective. Values intellectual partnership over romantic theatre. Shows love through trust and shared goals.'
      },
      INTP: {
        nickname: 'The Logician', icon: '⚛', color: 'linear-gradient(135deg, #6366f1, #06b6d4)',
        group: 'Analyst',
        overview: 'Curious, theoretical, and original. INTPs are inner inventors who chase the elegance of ideas more than their application.',
        strengths: ['Analytical depth', 'Originality', 'Open-mindedness', 'Comfortable with ambiguity', 'Honest reasoning'],
        weaknesses: ['Can over-think simple decisions', 'Procrastinates execution', 'Detached from emotional needs', 'Insensitive to social cues', 'Loses interest after the puzzle is solved'],
        communication: 'Precise, qualified, exploratory. Will rephrase your statement to make it sharper. Hates imprecise language.',
        leadership: 'Leads by ideas. Best as a thought leader or principal engineer; less effective at orchestrating people.',
        learning: 'Voracious, non-linear. Goes deep on whatever fascinates them. Resists rote learning.',
        workplace: 'Needs intellectual freedom and few interruptions. Best with flexible deadlines and complex problems.',
        careers: ['Researcher', 'Software developer', 'Mathematician', 'Philosopher', 'Data scientist'],
        teamwork: 'Excellent ideator; pair with execution-oriented teammates to ship.',
        stress: 'Becomes hyper-critical, retreats inward, and spirals into unproductive analysis loops.',
        growth: ['Set deadlines you actually keep', 'Tend to relationships before they wither', 'Acknowledge feelings as data, not noise'],
        famous: ['Albert Einstein', 'Isaac Newton', 'Bill Gates', 'Marie Curie'],
        relationships: 'Slow to commit, deeply loyal once they do. Values intellectual respect and personal space.'
      },
      ENTJ: {
        nickname: 'The Commander', icon: '⚔', color: 'linear-gradient(135deg, #dc2626, #7c2d12)',
        group: 'Analyst',
        overview: 'Bold, strategic, and natural leaders. ENTJs see inefficiency as a problem to be solved and aren\'t afraid to lead the charge.',
        strengths: ['Strategic vision', 'Confidence', 'Strong willpower', 'Efficient execution', 'Charismatic command'],
        weaknesses: ['Stubborn', 'Impatient', 'Can seem ruthless', 'Dismisses emotional concerns', 'Intolerant of incompetence'],
        communication: 'Direct, decisive, agenda-driven. Cuts through tangents. Expects the same.',
        leadership: 'Born executive. Sets vision, builds structure, drives accountability. Leads by example and expectation.',
        learning: 'Goal-oriented. Learns what serves the mission, fast.',
        workplace: 'Thrives in high-stakes, results-driven environments. Frustrated by indecision.',
        careers: ['CEO', 'Lawyer', 'Management consultant', 'Investment banker', 'Entrepreneur'],
        teamwork: 'Natural team captain. Pair with empathic colleagues to balance hard edges.',
        stress: 'Becomes domineering, dismissive, and impulsive. May steamroll others.',
        growth: ['Pause before reacting', 'Validate others\' feelings explicitly', 'Delegate without micromanaging'],
        famous: ['Steve Jobs', 'Margaret Thatcher', 'Gordon Ramsay', 'Franklin D. Roosevelt'],
        relationships: 'Committed, ambitious partners. Express affection through shared goals and growth.'
      },
      ENTP: {
        nickname: 'The Debater', icon: '⚡', color: 'linear-gradient(135deg, #ea580c, #facc15)',
        group: 'Analyst',
        overview: 'Quick, inventive, and provocative. ENTPs love to question assumptions, brainstorm wildly, and prototype the impossible.',
        strengths: ['Quick wit', 'Innovation', 'Charisma', 'Adaptable thinking', 'Comfort with conflict'],
        weaknesses: ['Argues for sport', 'Easily bored', 'Insensitive bluntness', 'Resists routine', 'Starts more than finishes'],
        communication: 'Playful, debate-loving. Will steelman the opposing view just to test it.',
        leadership: 'Inspires with ideas, energises with momentum. Less strong on follow-through.',
        learning: 'Wide-ranging and Socratic. Learns by arguing.',
        workplace: 'Needs novelty and intellectual sparring. Suffocates in static environments.',
        careers: ['Entrepreneur', 'Lawyer', 'Inventor', 'Marketing strategist', 'Journalist'],
        teamwork: 'The team\'s ideation engine. Pair with detail-oriented executors.',
        stress: 'Becomes chaotic, scattered, and combative. May abandon current obligations.',
        growth: ['Finish what you start', 'Pick your battles carefully', 'Listen for what people feel, not just what they say'],
        famous: ['Leonardo da Vinci', 'Mark Twain', 'Tom Hanks', 'Sacha Baron Cohen'],
        relationships: 'Exciting, unpredictable partners. Need intellectual stimulation and freedom.'
      },
      INFJ: {
        nickname: 'The Advocate', icon: '☯', color: 'linear-gradient(135deg, #059669, #14b8a6)',
        group: 'Diplomat',
        overview: 'Quietly idealistic visionaries. INFJs combine deep empathy with long-range insight, often pursuing meaningful causes.',
        strengths: ['Deep empathy', 'Insightful', 'Visionary', 'Determined', 'Quietly persuasive'],
        weaknesses: ['Burns out from caring too much', 'Sensitive to criticism', 'Avoids confrontation', 'Perfectionism', 'Hard to know fully'],
        communication: 'Warm, metaphor-rich, layered. Reads subtext effortlessly.',
        leadership: 'Mission-driven leadership. Inspires through purpose rather than power.',
        learning: 'Reflective, holistic. Connects new ideas to a personal worldview.',
        workplace: 'Needs meaningful work and a calm environment. Withers in cynical cultures.',
        careers: ['Counselor', 'Writer', 'Designer', 'Non-profit leader', 'Therapist'],
        teamwork: 'The team\'s conscience. Pair with action-oriented colleagues.',
        stress: 'Withdraws, ruminates, and may become uncharacteristically harsh.',
        growth: ['Set boundaries and protect your energy', 'Speak up before resentment builds', 'Accept good-enough over perfect'],
        famous: ['Carl Jung', 'Martin Luther King Jr.', 'Nelson Mandela', 'Lady Gaga'],
        relationships: 'Seeks soul-level connection. Loyal, deep, and rare to commit.'
      },
      INFP: {
        nickname: 'The Mediator', icon: '✿', color: 'linear-gradient(135deg, #10b981, #84cc16)',
        group: 'Diplomat',
        overview: 'Idealistic, creative, and values-driven. INFPs are quiet poets who care intensely about authenticity.',
        strengths: ['Empathic', 'Creative', 'Open-minded', 'Loyal to values', 'Adaptable in spirit'],
        weaknesses: ['Avoids conflict', 'Easily overwhelmed', 'Idealistic to a fault', 'Self-critical', 'Procrastinates on uninspiring tasks'],
        communication: 'Gentle, metaphorical, often through writing. Avoids confrontation.',
        leadership: 'Leads through inspiration and personal example, not authority.',
        learning: 'Curious and self-paced. Engages deeply with what aligns to their values.',
        workplace: 'Thrives in creative, values-aligned roles with autonomy.',
        careers: ['Writer', 'UX designer', 'Counselor', 'Artist', 'Teacher'],
        teamwork: 'The team\'s heart. Pair with grounded organisers.',
        stress: 'Becomes withdrawn, self-doubting, and overwhelmed by inner chaos.',
        growth: ['Take small actions even when uninspired', 'Voice disagreement directly', 'Accept imperfect reality alongside the ideal'],
        famous: ['William Shakespeare', 'J.R.R. Tolkien', 'Audrey Hepburn', 'Johnny Depp'],
        relationships: 'Devoted, idealistic partners who seek meaning and depth.'
      },
      ENFJ: {
        nickname: 'The Protagonist', icon: '★', color: 'linear-gradient(135deg, #d946ef, #f472b6)',
        group: 'Diplomat',
        overview: 'Charismatic and inspiring leaders who lift others up. ENFJs naturally see the potential in people and pull it forward.',
        strengths: ['Charismatic', 'Empathic', 'Persuasive', 'Reliable', 'Motivating'],
        weaknesses: ['Over-extends self', 'Avoids own needs', 'Sensitive to criticism', 'Idealistic blind spots', 'Approval-seeking'],
        communication: 'Warm, rallying, attuned. Reads the room exceptionally well.',
        leadership: 'Coaches and inspires. Builds movements out of meaning.',
        learning: 'Collaborative and human-centered. Engages through dialogue.',
        workplace: 'Excels in people-centered, mission-driven roles.',
        careers: ['Teacher', 'HR leader', 'Politician', 'Coach', 'Marketing director'],
        teamwork: 'Glue of the team. Pair with realists to balance idealism.',
        stress: 'Becomes self-sacrificing, anxious, and uncharacteristically critical.',
        growth: ['Tend to your own needs', 'Allow conflict when truth requires it', 'Detach worth from others\' approval'],
        famous: ['Barack Obama', 'Oprah Winfrey', 'Maya Angelou', 'Justin Trudeau'],
        relationships: 'Devoted, expressive, and supportive. May lose self in the relationship.'
      },
      ENFP: {
        nickname: 'The Campaigner', icon: '✺', color: 'linear-gradient(135deg, #f59e0b, #ec4899)',
        group: 'Diplomat',
        overview: 'Enthusiastic, creative free-spirits. ENFPs see possibilities in everything and people, and bring contagious energy.',
        strengths: ['Enthusiastic', 'Creative', 'Empathic', 'Sociable', 'Curious'],
        weaknesses: ['Easily distracted', 'Over-commits', 'Struggles with routine', 'Disorganised', 'Conflict-averse'],
        communication: 'Expressive, narrative, idea-bouncing. Talks fast, feels deeply.',
        leadership: 'Inspires with vision and energy. Less strong on operational discipline.',
        learning: 'Exploratory, story-driven. Loves variety.',
        workplace: 'Thrives in creative, varied, people-rich environments.',
        careers: ['Marketing creative', 'Journalist', 'Entrepreneur', 'Counselor', 'Producer'],
        teamwork: 'Team morale-booster. Pair with structured operators.',
        stress: 'Becomes scattered, anxious, and self-doubting; may shut down emotionally.',
        growth: ['Commit deeply to a few priorities', 'Build small daily systems', 'Address disagreements head-on'],
        famous: ['Robin Williams', 'Robert Downey Jr.', 'Walt Disney', 'Russell Brand'],
        relationships: 'Expressive, adventurous partners. Need novelty and emotional depth.'
      },
      ISTJ: {
        nickname: 'The Logistician', icon: '◈', color: 'linear-gradient(135deg, #475569, #1e293b)',
        group: 'Sentinel',
        overview: 'Practical, dependable, and tradition-respecting. ISTJs make sure things actually run — quietly and correctly.',
        strengths: ['Reliable', 'Detail-oriented', 'Disciplined', 'Honest', 'Patient'],
        weaknesses: ['Resistant to change', 'Stubborn', 'Judgmental of unconventional', 'Emotionally reserved', 'Inflexible'],
        communication: 'Plain, factual, brief. No embellishment.',
        leadership: 'Steward leadership — runs ships tightly through process and consistency.',
        learning: 'Sequential and applied. Masters fundamentals before advancing.',
        workplace: 'Thrives in structured, process-driven roles with clear expectations.',
        careers: ['Accountant', 'Auditor', 'Project manager', 'Civil engineer', 'Military officer'],
        teamwork: 'Backbone of the team. Pair with visionaries to spark new direction.',
        stress: 'Becomes rigid, withdrawn, and catastrophising about details.',
        growth: ['Try one new way of doing things', 'Express appreciation aloud', 'Consider intuition as input, not noise'],
        famous: ['George Washington', 'Warren Buffett', 'Queen Elizabeth II', 'Angela Merkel'],
        relationships: 'Steady, loyal partners who show love through reliability and acts of service.'
      },
      ISFJ: {
        nickname: 'The Defender', icon: '❀', color: 'linear-gradient(135deg, #0d9488, #65a30d)',
        group: 'Sentinel',
        overview: 'Warm, conscientious, and protective. ISFJs remember the small things and do the quiet work that holds groups together.',
        strengths: ['Supportive', 'Reliable', 'Observant', 'Patient', 'Loyal'],
        weaknesses: ['Self-sacrificing', 'Avoids conflict', 'Repressed feelings', 'Resistant to change', 'Takes things personally'],
        communication: 'Considerate, modest, indirect about own needs.',
        leadership: 'Servant leadership. Holds the team\'s wellbeing as a priority.',
        learning: 'Practical, observation-based. Learns by doing alongside.',
        workplace: 'Excels in supportive roles with clear expectations and appreciative culture.',
        careers: ['Nurse', 'Teacher', 'Social worker', 'Administrative manager', 'Counselor'],
        teamwork: 'The caretaker. Pair with assertive colleagues so their voice isn\'t lost.',
        stress: 'Burns out silently; may become anxious, withdrawn, or resentful.',
        growth: ['Voice your needs explicitly', 'Decline tasks beyond capacity', 'Welcome change as growth'],
        famous: ['Mother Teresa', 'Beyoncé', 'Kate Middleton', 'Rosa Parks'],
        relationships: 'Devoted, nurturing partners. Express love through care and small gestures.'
      },
      ESTJ: {
        nickname: 'The Executive', icon: '⬢', color: 'linear-gradient(135deg, #1e40af, #0891b2)',
        group: 'Sentinel',
        overview: 'Organised, decisive, and bound by duty. ESTJs run institutions like clockwork and uphold standards firmly.',
        strengths: ['Decisive', 'Organised', 'Loyal', 'Hardworking', 'Direct'],
        weaknesses: ['Inflexible', 'Stubborn', 'Judgmental', 'Difficulty with emotion', 'Dismissive of unconventional ideas'],
        communication: 'Direct, agenda-led, expectant of action.',
        leadership: 'Operational excellence. Sets standards, enforces accountability.',
        learning: 'Practical, structured. Wants outcomes you can measure.',
        workplace: 'Thrives in hierarchical, process-driven environments.',
        careers: ['Operations director', 'Judge', 'Police officer', 'Banker', 'Chief of staff'],
        teamwork: 'The enforcer. Pair with creative challengers to avoid stagnation.',
        stress: 'Becomes controlling, blunt, and dismissive of feelings.',
        growth: ['Pause before correcting others', 'Consider feelings as relevant input', 'Stay open to new methods'],
        famous: ['Frank Sinatra', 'Sonia Sotomayor', 'Lyndon B. Johnson', 'Judge Judy'],
        relationships: 'Steadfast, traditional, dependable partners.'
      },
      ESFJ: {
        nickname: 'The Consul', icon: '✦', color: 'linear-gradient(135deg, #f43f5e, #f97316)',
        group: 'Sentinel',
        overview: 'Caring, social, and community-minded. ESFJs are the hosts and helpers who keep the social fabric warm.',
        strengths: ['Warm', 'Loyal', 'Practical', 'Supportive', 'Strong sense of duty'],
        weaknesses: ['Approval-seeking', 'Inflexible', 'Sensitive to criticism', 'Reluctant to innovate', 'Self-righteous when crossed'],
        communication: 'Warm, relational, attentive. Uses connection to lead.',
        leadership: 'Hands-on, people-first. Leads through shared values and care.',
        learning: 'Collaborative, applied. Learns alongside others.',
        workplace: 'Thrives in people-rich, supportive environments with clear roles.',
        careers: ['HR manager', 'Healthcare administrator', 'Event manager', 'Teacher', 'Sales lead'],
        teamwork: 'The host and connector. Pair with strategic thinkers.',
        stress: 'Becomes anxious, controlling, or martyred when unappreciated.',
        growth: ['Own your needs openly', 'Sit with disagreement without rushing harmony', 'Try unfamiliar ideas before judging them'],
        famous: ['Taylor Swift', 'Jennifer Garner', 'Bill Clinton', 'Hugh Jackman'],
        relationships: 'Devoted, attentive, traditional partners. Show love through service.'
      },
      ISTP: {
        nickname: 'The Virtuoso', icon: '⚙', color: 'linear-gradient(135deg, #64748b, #0ea5e9)',
        group: 'Explorer',
        overview: 'Practical, hands-on problem solvers. ISTPs love taking things apart, fixing problems, and mastering tools.',
        strengths: ['Practical', 'Calm under pressure', 'Independent', 'Adaptable', 'Resourceful'],
        weaknesses: ['Emotionally reserved', 'Easily bored', 'Risk-prone', 'Avoids commitment', 'Dismissive of feelings'],
        communication: 'Sparse, factual, action-over-words.',
        leadership: 'Quietly capable. Leads by doing.',
        learning: 'Hands-on, tactile. Learns by tinkering.',
        workplace: 'Thrives in autonomous, hands-on, problem-solving roles.',
        careers: ['Engineer', 'Pilot', 'Mechanic', 'Surgeon', 'Forensic analyst'],
        teamwork: 'The fixer. Pair with planners and motivators.',
        stress: 'Becomes withdrawn or impulsively reckless.',
        growth: ['Commit to long-range plans', 'Express appreciation explicitly', 'Engage with abstract ideas'],
        famous: ['Clint Eastwood', 'Tom Cruise', 'Bear Grylls', 'Frida Kahlo'],
        relationships: 'Independent, action-loving partners. Show love by fixing and providing.'
      },
      ISFP: {
        nickname: 'The Adventurer', icon: '✧', color: 'linear-gradient(135deg, #ec4899, #fb923c)',
        group: 'Explorer',
        overview: 'Gentle, sensitive artists with a deep aesthetic sense. ISFPs live in the moment and express themselves through what they make.',
        strengths: ['Sensitive', 'Artistic', 'Loyal', 'Adaptable', 'Charming'],
        weaknesses: ['Avoids conflict', 'Independent to a fault', 'Easily stressed', 'Difficulty planning ahead', 'Self-doubting'],
        communication: 'Quiet, gentle, often non-verbal expression.',
        leadership: 'Leads by example and sensitivity, not authority.',
        learning: 'Experiential, sensory. Learns through doing and feeling.',
        workplace: 'Needs creative freedom, low conflict, and aesthetic environments.',
        careers: ['Artist', 'Designer', 'Veterinarian', 'Chef', 'Photographer'],
        teamwork: 'The aesthetic eye. Pair with planners.',
        stress: 'Withdraws, becomes overly self-critical, may snap suddenly.',
        growth: ['Plan a few steps ahead', 'Voice disagreements early', 'Treat criticism as data, not attack'],
        famous: ['Bob Dylan', 'Britney Spears', 'Lana Del Rey', 'Michael Jackson'],
        relationships: 'Sensitive, devoted, present-focused partners.'
      },
      ESTP: {
        nickname: 'The Entrepreneur', icon: '⚡', color: 'linear-gradient(135deg, #f97316, #dc2626)',
        group: 'Explorer',
        overview: 'Energetic, perceptive, action-driven. ESTPs read a situation in seconds and make moves while others are still thinking.',
        strengths: ['Bold', 'Practical', 'Sociable', 'Pragmatic', 'Quick-thinking'],
        weaknesses: ['Impatient', 'Risk-prone', 'Dismissive of theory', 'Insensitive', 'Avoids long-term planning'],
        communication: 'Direct, action-oriented, witty.',
        leadership: 'Frontline leader. Calm in chaos, fast to decide.',
        learning: 'Hands-on. Bored by theory.',
        workplace: 'Thrives in fast-moving, high-stakes, real-world roles.',
        careers: ['Sales executive', 'Paramedic', 'Athlete', 'Trader', 'Entrepreneur'],
        teamwork: 'The action engine. Pair with planners and reflective thinkers.',
        stress: 'Becomes impulsive and reckless; may abandon obligations.',
        growth: ['Plan further out than next week', 'Listen for feelings beneath behavior', 'Stay with theoretical ideas longer'],
        famous: ['Madonna', 'Donald Trump', 'Eddie Murphy', 'Ernest Hemingway'],
        relationships: 'Exciting, present-focused partners. Show love through shared adventure.'
      },
      ESFP: {
        nickname: 'The Entertainer', icon: '☼', color: 'linear-gradient(135deg, #fbbf24, #f43f5e)',
        group: 'Explorer',
        overview: 'Warm, lively, and crowd-pleasing. ESFPs turn moments into experiences and bring joy wherever they go.',
        strengths: ['Energetic', 'Warm', 'Observant', 'Practical', 'Spontaneous'],
        weaknesses: ['Easily distracted', 'Conflict-averse', 'Short-term focused', 'Sensitive to criticism', 'Difficulty planning'],
        communication: 'Warm, expressive, in-the-moment.',
        leadership: 'Energising. Leads through morale and shared experience.',
        learning: 'Experiential and social.',
        workplace: 'Thrives in lively, people-rich, expressive roles.',
        careers: ['Performer', 'Hospitality manager', 'Sales representative', 'Designer', 'Teacher'],
        teamwork: 'The energiser. Pair with detail-oriented planners.',
        stress: 'Becomes overwhelmed, anxious, and unusually pessimistic.',
        growth: ['Plan a few weeks out', 'Sit with hard feedback before reacting', 'Build small daily disciplines'],
        famous: ['Marilyn Monroe', 'Adele', 'Elvis Presley', 'Will Smith'],
        relationships: 'Affectionate, expressive, present-focused partners.'
      }
    },

    typeOrder: ['ISTJ','ISFJ','INFJ','INTJ','ISTP','ISFP','INFP','INTP','ESTP','ESFP','ENFP','ENTP','ESTJ','ESFJ','ENFJ','ENTJ'],

    badges: [
      { id: 'first_step', name: 'First Step', icon: '🌱', desc: 'Answer your first question.' },
      { id: 'halfway', name: 'Halfway There', icon: '🚀', desc: 'Reach the midpoint of the assessment.' },
      { id: 'self_aware', name: 'Self-Aware', icon: '🪞', desc: 'Complete the assessment.' },
      { id: 'explorer', name: 'Explorer', icon: '🗺', desc: 'View all 16 type profiles.' },
      { id: 'matchmaker', name: 'Matchmaker', icon: '💞', desc: 'Run 5 compatibility checks.' },
      { id: 'returning', name: 'Returning Insight', icon: '🔁', desc: 'Complete a second assessment.' },
      { id: 'theme_dancer', name: 'Theme Dancer', icon: '🌓', desc: 'Toggle the theme.' }
    ]
  };

  /* =============================================================
     STORAGE
     ============================================================= */
  MBTI.Storage = (() => {
    const K = {
      progress: 'mbti.progress',
      history: 'mbti.history',
      theme: 'mbti.theme',
      sound: 'mbti.sound',
      xp: 'mbti.xp',
      lastResult: 'mbti.lastResult',
      typesViewed: 'mbti.typesViewed',
      compatRuns: 'mbti.compatRuns'
    };
    function get(k, d) {
      try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); }
      catch (e) { return d; }
    }
    function set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
    function del(k) { try { localStorage.removeItem(k); } catch (e) {} }
    return { K, get, set, del };
  })();

  /* =============================================================
     SCORING
     ============================================================= */
  MBTI.Scoring = {
    score(answers) {
      const sums = { EI: 0, SN: 0, TF: 0, JP: 0 };
      const max = { EI: 0, SN: 0, TF: 0, JP: 0 };
      MBTI.Data.questions.forEach((q, i) => {
        const a = answers[i];
        max[q.d] += 2;
        if (a == null) return;
        sums[q.d] += a * q.dir;
      });
      // Positive sum → dim.a (E, N, T, J); negative → dim.b (I, S, F, P)
      const pick = (code) => {
        const dim = MBTI.Data.dimensions.find(d => d.code === code);
        return sums[code] >= 0 ? dim.a : dim.b;
      };
      const type = pick('EI') + pick('SN') + pick('TF') + pick('JP');
      const strengths = {};
      MBTI.Data.dimensions.forEach(d => {
        const pct = max[d.code] === 0 ? 50 : Math.round((Math.abs(sums[d.code]) / max[d.code]) * 50 + 50);
        const letter = sums[d.code] >= 0 ? d.a : d.b;
        strengths[letter] = pct;
      });
      return { type, scores: sums, max, strengths };
    }
  };

  /* =============================================================
     UI HELPERS
     ============================================================= */
  MBTI.UI = (() => {
    let toastTimer = null;
    function toast(msg) {
      const el = document.getElementById('toast');
      el.textContent = msg;
      el.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => el.classList.remove('show'), 2400);
    }
    function fireConfetti() {
      if (typeof confetti !== 'function') return;
      const burst = (opts) => confetti(Object.assign({
        particleCount: 80, spread: 70, origin: { y: 0.7 },
        colors: ['#a78bfa', '#22d3ee', '#f472b6', '#fbbf24']
      }, opts));
      burst({ angle: 60, origin: { x: 0, y: 0.7 } });
      burst({ angle: 120, origin: { x: 1, y: 0.7 } });
      setTimeout(() => burst({ particleCount: 120, spread: 120, origin: { y: 0.6 } }), 200);
    }
    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      MBTI.Storage.set(MBTI.Storage.K.theme, theme);
      const ic = document.querySelector('[data-theme-icon]');
      if (ic) ic.textContent = theme === 'dark' ? '☾' : '☀';
    }
    function initTheme() {
      const saved = MBTI.Storage.get(MBTI.Storage.K.theme, 'dark');
      setTheme(saved);
      document.getElementById('theme-toggle').addEventListener('click', () => {
        const cur = document.documentElement.getAttribute('data-theme');
        setTheme(cur === 'dark' ? 'light' : 'dark');
        MBTI.Gamification.unlock('theme_dancer');
      });
    }
    let soundOn = true;
    function initSound() {
      soundOn = MBTI.Storage.get(MBTI.Storage.K.sound, true);
      updateSoundIcon();
      document.getElementById('sound-toggle').addEventListener('click', () => {
        soundOn = !soundOn;
        MBTI.Storage.set(MBTI.Storage.K.sound, soundOn);
        updateSoundIcon();
        if (soundOn) playTick();
      });
    }
    function updateSoundIcon() {
      const el = document.querySelector('[data-sound-on]');
      if (el) el.textContent = soundOn ? '🔊' : '🔇';
    }
    let audioCtx;
    function playTick(freq = 440) {
      if (!soundOn) return;
      try {
        audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
        const o = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        o.frequency.value = freq;
        o.type = 'sine';
        g.gain.value = 0.05;
        o.connect(g); g.connect(audioCtx.destination);
        o.start();
        g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.18);
        o.stop(audioCtx.currentTime + 0.2);
      } catch (e) {}
    }
    function playChime() {
      [523, 659, 784].forEach((f, i) => setTimeout(() => playTick(f), i * 120));
    }
    return { toast, fireConfetti, initTheme, initSound, playTick, playChime };
  })();

  /* =============================================================
     ROUTER
     ============================================================= */
  MBTI.Router = (() => {
    const routes = ['landing', 'assessment', 'results', 'types', 'compatibility', 'history'];
    function go(name) {
      if (!routes.includes(name)) name = 'landing';
      document.querySelectorAll('.view').forEach(v => v.classList.toggle('active', v.dataset.view === name));
      document.querySelectorAll('.nav a').forEach(a => a.classList.toggle('active', a.dataset.route === name));
      window.scrollTo({ top: 0, behavior: 'smooth' });
      if (location.hash !== '#' + name) location.hash = name;
      // close mobile nav
      document.querySelector('.nav')?.classList.remove('open');
      // Lifecycle
      if (name === 'assessment') MBTI.Assessment.show();
      if (name === 'results') MBTI.Results.show();
      if (name === 'types') MBTI.Types.renderGrid();
      if (name === 'compatibility') MBTI.Compatibility.show();
      if (name === 'history') MBTI.History.show();
    }
    function init() {
      window.addEventListener('hashchange', () => go(location.hash.slice(1)));
      document.body.addEventListener('click', (e) => {
        const a = e.target.closest('[data-route]');
        if (!a) return;
        e.preventDefault();
        go(a.dataset.route);
      });
      go(location.hash.slice(1) || 'landing');
    }
    return { init, go };
  })();

  /* =============================================================
     GAMIFICATION
     ============================================================= */
  MBTI.Gamification = (() => {
    function state() { return MBTI.Storage.get(MBTI.Storage.K.xp, { points: 0, badges: [] }); }
    function save(s) { MBTI.Storage.set(MBTI.Storage.K.xp, s); render(); }
    function addXP(n) {
      const s = state();
      s.points = (s.points || 0) + n;
      save(s);
    }
    function unlock(id) {
      const s = state();
      if (!s.badges.includes(id)) {
        s.badges.push(id);
        const b = MBTI.Data.badges.find(b => b.id === id);
        if (b) MBTI.UI.toast(`${b.icon}  Badge unlocked: ${b.name}`);
        save(s);
      }
    }
    function render() {
      const s = state();
      const xp = document.getElementById('xp-count');
      if (xp) xp.textContent = s.points || 0;
      const wrap = document.getElementById('badges');
      if (wrap) {
        wrap.innerHTML = MBTI.Data.badges.map(b => `
          <div class="badge ${s.badges.includes(b.id) ? 'unlocked' : ''}" title="${b.desc}">
            <div class="b-icon">${b.icon}</div>
            <div class="b-name">${b.name}</div>
          </div>
        `).join('');
      }
    }
    return { addXP, unlock, render, state };
  })();

  /* =============================================================
     LANDING
     ============================================================= */
  MBTI.Landing = (() => {
    function render() {
      // Dimension cards
      const dimGrid = document.getElementById('dim-grid');
      dimGrid.innerHTML = MBTI.Data.dimensions.map(d => `
        <div class="dim-card">
          <div class="dim-letters">${d.a} ↔ ${d.b}</div>
          <h3>${d.aName} vs ${d.bName}</h3>
          <p>${d.desc}</p>
        </div>
      `).join('');
      // Types preview (8)
      const grid = document.getElementById('landing-types-grid');
      grid.innerHTML = MBTI.Data.typeOrder.slice(0, 8).map(typeCardHTML).join('');
      grid.addEventListener('click', onTypeClick);
    }
    function typeCardHTML(t) {
      const p = MBTI.Data.types[t];
      return `<button class="type-card" data-type="${t}" style="--type-color: ${p.color}">
        <div class="type-icon">${p.icon}</div>
        <div class="type-letters">${t}</div>
        <h4>${p.nickname}</h4>
        <p>${p.overview.split('.')[0]}.</p>
        <span class="type-group">${p.group}</span>
      </button>`;
    }
    function onTypeClick(e) {
      const card = e.target.closest('.type-card');
      if (card) MBTI.Types.openModal(card.dataset.type);
    }
    return { render, typeCardHTML };
  })();

  /* =============================================================
     ASSESSMENT
     ============================================================= */
  MBTI.Assessment = (() => {
    let idx = 0;
    let answers = [];
    function load() {
      const saved = MBTI.Storage.get(MBTI.Storage.K.progress, null);
      if (saved && Array.isArray(saved.answers)) {
        answers = saved.answers;
        idx = Math.min(saved.idx || 0, MBTI.Data.questions.length - 1);
      } else {
        answers = new Array(MBTI.Data.questions.length).fill(null);
        idx = 0;
      }
    }
    function save() {
      MBTI.Storage.set(MBTI.Storage.K.progress, { answers, idx });
      const a = document.getElementById('auto-save');
      if (a) { a.textContent = 'Auto-saved ✓'; setTimeout(() => a.textContent = 'Auto-saved', 800); }
    }
    function show() {
      load();
      render();
      bindOnce();
    }
    let bound = false;
    function bindOnce() {
      if (bound) return; bound = true;
      document.getElementById('prev-btn').addEventListener('click', prev);
      document.getElementById('next-btn').addEventListener('click', next);
      document.getElementById('reset-assessment').addEventListener('click', () => {
        if (confirm('Reset all progress and start over?')) {
          MBTI.Storage.del(MBTI.Storage.K.progress);
          load(); render();
          MBTI.UI.toast('Assessment reset');
        }
      });
      document.getElementById('likert').addEventListener('click', (e) => {
        const b = e.target.closest('.likert-btn');
        if (!b) return;
        const v = parseInt(b.dataset.value, 10);
        const wasUnanswered = answers[idx] == null;
        answers[idx] = v;
        save();
        renderLikert();
        MBTI.UI.playTick(420 + v * 30);
        if (wasUnanswered) {
          MBTI.Gamification.addXP(10);
          if (idx === 0) MBTI.Gamification.unlock('first_step');
          if (idx === Math.floor(MBTI.Data.questions.length / 2)) MBTI.Gamification.unlock('halfway');
        }
        // Auto-advance
        setTimeout(() => next(), 240);
      });
      document.addEventListener('keydown', (e) => {
        if (!document.querySelector('[data-view="assessment"]').classList.contains('active')) return;
        if (e.key === 'ArrowRight') next();
        if (e.key === 'ArrowLeft') prev();
        const map = { '1': 2, '2': 1, '3': 0, '4': -1, '5': -2 };
        if (map.hasOwnProperty(e.key)) {
          const btn = document.querySelector(`.likert-btn[data-value="${map[e.key]}"]`);
          if (btn) btn.click();
        }
      });
    }
    function render() {
      const q = MBTI.Data.questions[idx];
      const total = MBTI.Data.questions.length;
      document.getElementById('q-counter').textContent = `${idx + 1} / ${total}`;
      const dim = MBTI.Data.dimensions.find(d => d.code === q.d);
      document.getElementById('dim-label').textContent = `${dim.aName} ↔ ${dim.bName}`;
      document.getElementById('question-text').textContent = q.t;
      const pct = Math.round(((idx) / total) * 100);
      document.getElementById('progress-fill').style.width = pct + '%';
      document.getElementById('progress-pct').textContent = pct + '%';
      document.getElementById('prev-btn').disabled = idx === 0;
      document.getElementById('next-btn').textContent = idx === total - 1 ? 'Finish →' : 'Next →';
      renderLikert();
    }
    function renderLikert() {
      const cur = answers[idx];
      document.querySelectorAll('.likert-btn').forEach(b => {
        b.classList.toggle('selected', parseInt(b.dataset.value, 10) === cur);
      });
    }
    function next() {
      if (idx < MBTI.Data.questions.length - 1) {
        idx++; save(); render();
      } else {
        finish();
      }
    }
    function prev() {
      if (idx > 0) { idx--; save(); render(); }
    }
    function finish() {
      const total = MBTI.Data.questions.length;
      const answered = answers.filter(a => a != null).length;
      if (answered < total) {
        const next = answers.findIndex(a => a == null);
        idx = next >= 0 ? next : idx;
        save(); render();
        MBTI.UI.toast(`Please answer all ${total} questions (${total - answered} left).`);
        return;
      }
      const result = MBTI.Scoring.score(answers);
      const record = { type: result.type, strengths: result.strengths, scores: result.scores, ts: Date.now() };
      MBTI.Storage.set(MBTI.Storage.K.lastResult, record);
      const hist = MBTI.Storage.get(MBTI.Storage.K.history, []);
      const isReturning = hist.length > 0;
      hist.unshift(record);
      MBTI.Storage.set(MBTI.Storage.K.history, hist.slice(0, 20));
      MBTI.Gamification.addXP(200);
      MBTI.Gamification.unlock('self_aware');
      if (isReturning) MBTI.Gamification.unlock('returning');
      MBTI.Storage.del(MBTI.Storage.K.progress);
      MBTI.Router.go('results');
    }
    return { show };
  })();

  /* =============================================================
     RESULTS
     ============================================================= */
  MBTI.Results = (() => {
    let chartInstance = null;
    function show() {
      const r = MBTI.Storage.get(MBTI.Storage.K.lastResult, null);
      if (!r) {
        document.getElementById('result-hero').innerHTML = `
          <h2>No result yet</h2>
          <p class="muted" style="margin:14px 0 24px">Take the assessment to see your profile.</p>
          <button class="btn btn-primary" data-route="assessment">Start Assessment</button>`;
        document.querySelector('.result-grid').style.display = 'none';
        document.querySelector('.insights-card').style.display = 'none';
        document.querySelector('.compat-strip').parentElement.style.display = 'none';
        document.querySelector('.result-actions').style.display = 'none';
        return;
      }
      document.querySelector('.result-grid').style.display = '';
      document.querySelector('.insights-card').style.display = '';
      document.querySelector('.compat-strip').parentElement.style.display = '';
      document.querySelector('.result-actions').style.display = '';

      renderHero(r);
      renderTraits(r);
      renderRadar(r);
      renderInsights(r, 'strengths');
      renderCompatStrip(r);
      bindOnce();
      setTimeout(() => MBTI.UI.fireConfetti(), 250);
      MBTI.UI.playChime();
    }
    function renderHero(r) {
      const p = MBTI.Data.types[r.type];
      document.getElementById('result-hero').innerHTML = `
        <div class="type-icon">${p.icon}</div>
        <div class="type-big">${r.type}</div>
        <div class="type-nick">${p.nickname}</div>
        <p class="type-overview">${p.overview}</p>
      `;
    }
    function renderTraits(r) {
      const wrap = document.getElementById('trait-bars');
      wrap.innerHTML = MBTI.Data.dimensions.map(d => {
        const sum = r.scores[d.code];
        const max = MBTI.Data.questions.filter(q => q.d === d.code).length * 2;
        const ratio = (sum + max) / (max * 2); // 0..1, 0.5 center
        const pct = Math.round(ratio * 100);
        const winner = sum >= 0 ? d.a : d.b;
        const flipped = winner === d.b;
        const strengthPct = r.strengths[winner];
        return `
          <div class="trait-row ${flipped ? 'flipped' : ''}">
            <div class="left">${d.aName} (${d.a})</div>
            <div class="trait-track">
              <span class="center"></span>
              <span class="marker" style="left:${pct}%"></span>
            </div>
            <div class="right">${d.bName} (${d.b})</div>
            <div style="grid-column: 1 / -1; font-size: 0.78rem; color: var(--text-dim); text-align:center; margin-top: -6px">${winner} • ${strengthPct}% strength</div>
          </div>`;
      }).join('');
    }
    function renderRadar(r) {
      const ctx = document.getElementById('radar-chart');
      if (!ctx || typeof Chart === 'undefined') return;
      if (chartInstance) chartInstance.destroy();
      const labels = MBTI.Data.dimensions.map(d => {
        const winner = r.scores[d.code] >= 0 ? d.a : d.b;
        return `${winner} (${d[winner === d.a ? 'aName' : 'bName']})`;
      });
      const data = MBTI.Data.dimensions.map(d => {
        const winner = r.scores[d.code] >= 0 ? d.a : d.b;
        return r.strengths[winner];
      });
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const grid = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)';
      const tick = isDark ? '#a4a4b8' : '#4a4a66';
      chartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
          labels,
          datasets: [{
            label: 'Strength',
            data,
            backgroundColor: 'rgba(167,139,250,0.25)',
            borderColor: '#a78bfa',
            pointBackgroundColor: '#22d3ee',
            pointRadius: 5,
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            r: {
              suggestedMin: 0, suggestedMax: 100,
              ticks: { color: tick, backdropColor: 'transparent', stepSize: 25 },
              angleLines: { color: grid },
              grid: { color: grid },
              pointLabels: { color: tick, font: { size: 11, family: 'Inter' } }
            }
          }
        }
      });
    }
    function renderInsights(r, tab) {
      const p = MBTI.Data.types[r.type];
      const body = document.getElementById('insight-body');
      const arr = (xs) => `<ul>${xs.map(x => `<li>${x}</li>`).join('')}</ul>`;
      const map = {
        strengths: arr(p.strengths),
        weaknesses: arr(p.weaknesses),
        communication: `<p>${p.communication}</p>`,
        leadership: `<p>${p.leadership}</p>`,
        learning: `<p>${p.learning}</p>`,
        workplace: `<p>${p.workplace}</p>`,
        careers: arr(p.careers),
        teamwork: `<p>${p.teamwork}</p>`,
        stress: `<p>${p.stress}</p>`,
        growth: arr(p.growth)
      };
      body.innerHTML = map[tab] || '';
      document.querySelectorAll('#insight-tabs .tab').forEach(t => {
        t.classList.toggle('active', t.dataset.tab === tab);
      });
    }
    function renderCompatStrip(r) {
      const strip = document.getElementById('compat-strip');
      const matches = MBTI.Compatibility.topMatches(r.type, 4);
      strip.innerHTML = matches.map(m => {
        const p = MBTI.Data.types[m.type];
        return `<button class="compat-pill" data-route="compatibility" data-pair="${r.type}|${m.type}">
          <div class="ct">${m.type}</div>
          <div class="cn">${p.nickname}</div>
          <div class="cs">${m.score}% • ${m.label}</div>
        </button>`;
      }).join('');
    }
    let bound = false;
    function bindOnce() {
      if (bound) return; bound = true;
      document.getElementById('insight-tabs').addEventListener('click', (e) => {
        const t = e.target.closest('.tab');
        if (!t) return;
        const r = MBTI.Storage.get(MBTI.Storage.K.lastResult, null);
        if (r) renderInsights(r, t.dataset.tab);
      });
      document.getElementById('retake-btn').addEventListener('click', () => {
        if (confirm('Retake the assessment from the start?')) {
          MBTI.Storage.del(MBTI.Storage.K.progress);
          MBTI.Router.go('assessment');
        }
      });
      document.getElementById('share-btn').addEventListener('click', share);
      document.getElementById('download-btn').addEventListener('click', download);
      document.getElementById('compat-strip').addEventListener('click', (e) => {
        const pill = e.target.closest('[data-pair]');
        if (!pill) return;
        const [a, b] = pill.dataset.pair.split('|');
        MBTI.Compatibility.preset(a, b);
      });
    }
    async function share() {
      const r = MBTI.Storage.get(MBTI.Storage.K.lastResult, null);
      if (!r) return;
      const p = MBTI.Data.types[r.type];
      const text = `I'm ${r.type} — ${p.nickname}. ${p.overview}\nDiscover yours on Persona.`;
      if (navigator.share) {
        try { await navigator.share({ title: 'My MBTI Result', text }); return; } catch (e) {}
      }
      try { await navigator.clipboard.writeText(text); MBTI.UI.toast('Result copied to clipboard'); }
      catch (e) { MBTI.UI.toast('Sharing not supported on this browser'); }
    }
    async function download() {
      const node = document.querySelector('.results-shell');
      if (!node || typeof html2canvas !== 'function') {
        MBTI.UI.toast('Download not available'); return;
      }
      MBTI.UI.toast('Rendering image…');
      try {
        const canvas = await html2canvas(node, { backgroundColor: getComputedStyle(document.body).backgroundColor, scale: 2, useCORS: true });
        const link = document.createElement('a');
        link.download = `persona-${MBTI.Storage.get(MBTI.Storage.K.lastResult).type}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
      } catch (e) {
        MBTI.UI.toast('Could not render image');
      }
    }
    return { show };
  })();

  /* =============================================================
     TYPES
     ============================================================= */
  MBTI.Types = (() => {
    let activeFilter = 'All';
    function renderGrid() {
      renderFilter();
      const grid = document.getElementById('types-grid');
      const types = MBTI.Data.typeOrder.filter(t => activeFilter === 'All' || MBTI.Data.types[t].group === activeFilter);
      grid.innerHTML = types.map(MBTI.Landing.typeCardHTML).join('');
      grid.onclick = (e) => {
        const c = e.target.closest('.type-card');
        if (c) openModal(c.dataset.type);
      };
    }
    function renderFilter() {
      const groups = ['All', 'Analyst', 'Diplomat', 'Sentinel', 'Explorer'];
      const wrap = document.getElementById('type-filter');
      wrap.innerHTML = groups.map(g => `<button data-g="${g}" class="${g === activeFilter ? 'active' : ''}">${g}</button>`).join('');
      wrap.onclick = (e) => {
        const b = e.target.closest('button');
        if (!b) return;
        activeFilter = b.dataset.g;
        renderGrid();
      };
    }
    function openModal(t) {
      const p = MBTI.Data.types[t];
      const body = document.getElementById('type-modal-body');
      const arr = (xs) => `<ul>${xs.map(x => `<li>${x}</li>`).join('')}</ul>`;
      const chips = (xs) => `<div class="chip-row">${xs.map(x => `<span class="chip">${x}</span>`).join('')}</div>`;
      body.innerHTML = `
        <div class="type-icon" style="font-size:2.2rem">${p.icon}</div>
        <h2>${t}</h2>
        <div class="nick">${p.nickname} · <em>${p.group}</em></div>
        <div class="field"><h4>Overview</h4><p>${p.overview}</p></div>
        <div class="field"><h4>Strengths</h4>${arr(p.strengths)}</div>
        <div class="field"><h4>Weaknesses</h4>${arr(p.weaknesses)}</div>
        <div class="field"><h4>Communication</h4><p>${p.communication}</p></div>
        <div class="field"><h4>Leadership</h4><p>${p.leadership}</p></div>
        <div class="field"><h4>Learning</h4><p>${p.learning}</p></div>
        <div class="field"><h4>Workplace</h4><p>${p.workplace}</p></div>
        <div class="field"><h4>Career paths</h4>${chips(p.careers)}</div>
        <div class="field"><h4>Team contribution</h4><p>${p.teamwork}</p></div>
        <div class="field"><h4>Under stress</h4><p>${p.stress}</p></div>
        <div class="field"><h4>Growth path</h4>${arr(p.growth)}</div>
        <div class="field"><h4>Relationships</h4><p>${p.relationships}</p></div>
        <div class="field"><h4>Famous ${t}s</h4>${chips(p.famous)}</div>
      `;
      document.getElementById('type-modal').classList.add('open');
      document.getElementById('type-modal').setAttribute('aria-hidden', 'false');
      // Track viewing
      const seen = MBTI.Storage.get(MBTI.Storage.K.typesViewed, []);
      if (!seen.includes(t)) {
        seen.push(t);
        MBTI.Storage.set(MBTI.Storage.K.typesViewed, seen);
        MBTI.Gamification.addXP(50);
        if (seen.length === MBTI.Data.typeOrder.length) MBTI.Gamification.unlock('explorer');
      }
    }
    function init() {
      const modal = document.getElementById('type-modal');
      modal.addEventListener('click', (e) => {
        if (e.target.matches('[data-close]')) {
          modal.classList.remove('open');
          modal.setAttribute('aria-hidden', 'true');
        }
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          modal.classList.remove('open');
          modal.setAttribute('aria-hidden', 'true');
        }
      });
    }
    return { renderGrid, openModal, init };
  })();

  /* =============================================================
     COMPATIBILITY
     ============================================================= */
  MBTI.Compatibility = (() => {
    // Rule-based score
    function score(a, b) {
      if (a === b) return { score: 78, label: 'Mirror', tip: 'Same type — instant understanding, but you\'ll share blind spots. Diversify perspectives outside this pair.' };
      let s = 50;
      // shared S/N is the biggest signal in MBTI compatibility lore
      if (a[1] === b[1]) s += 18; else s -= 6;
      // shared T/F: warm friction or shared tone
      if (a[2] === b[2]) s += 8; else s += 4; // mixed T/F can complement
      // E/I balance — opposite often complements, same is comfortable
      if (a[0] !== b[0]) s += 6; else s += 3;
      // J/P balance — opposite tends to balance follow-through with flexibility
      if (a[3] !== b[3]) s += 8; else s += 4;
      // classic "ideal partner" theory: invert E/I and J/P, share S/N, oppose T/F
      if (a[1] === b[1] && a[0] !== b[0] && a[3] !== b[3] && a[2] !== b[2]) s += 12;
      s = Math.max(35, Math.min(98, s));
      let label;
      if (s >= 85) label = 'Excellent';
      else if (s >= 72) label = 'Strong';
      else if (s >= 58) label = 'Good';
      else label = 'Challenging';
      const tip = tipFor(a, b, s, label);
      return { score: s, label, tip };
    }
    function tipFor(a, b, s, label) {
      const sameSN = a[1] === b[1];
      const sameTF = a[2] === b[2];
      const sameEI = a[0] === b[0];
      const sameJP = a[3] === b[3];
      if (label === 'Excellent') return `${a} and ${b} share a worldview${sameSN ? ' through their information style' : ''}, while differing just enough to balance each other. Lean into your complementary decision and lifestyle preferences.`;
      if (label === 'Strong') return `${a} and ${b} are likely to click, especially when they bring distinct strengths. Watch for ${sameTF ? 'shared blind spots in feedback' : 'friction in how decisions feel right'}.`;
      if (label === 'Good') return `${a} and ${b} can collaborate well with awareness. ${!sameSN ? 'Differences in how you take in information may need translation.' : ''} Make implicit assumptions explicit.`;
      return `${a} and ${b} can grow together but expect friction. ${!sameSN ? 'Different information styles mean you may literally talk past each other.' : ''} Schedule explicit alignment moments.`;
    }
    function topMatches(a, n = 4) {
      return MBTI.Data.typeOrder
        .filter(t => t !== a)
        .map(t => Object.assign({ type: t }, score(a, t)))
        .sort((x, y) => y.score - x.score)
        .slice(0, n);
    }
    function show() {
      const sa = document.getElementById('compat-a');
      const sb = document.getElementById('compat-b');
      if (!sa.options.length) {
        const opts = MBTI.Data.typeOrder.map(t => `<option value="${t}">${t} — ${MBTI.Data.types[t].nickname}</option>`).join('');
        sa.innerHTML = opts; sb.innerHTML = opts;
        const last = MBTI.Storage.get(MBTI.Storage.K.lastResult, null);
        if (last) sa.value = last.type;
        sb.value = MBTI.Data.typeOrder.find(t => t !== sa.value);
        sa.addEventListener('change', update);
        sb.addEventListener('change', update);
      }
      update();
      renderMatrix();
    }
    function preset(a, b) {
      MBTI.Router.go('compatibility');
      setTimeout(() => {
        document.getElementById('compat-a').value = a;
        document.getElementById('compat-b').value = b;
        update();
      }, 60);
    }
    function update() {
      const a = document.getElementById('compat-a').value;
      const b = document.getElementById('compat-b').value;
      const r = score(a, b);
      const pa = MBTI.Data.types[a];
      const pb = MBTI.Data.types[b];
      document.getElementById('compat-result').innerHTML = `
        <div class="compat-pair">
          <div class="pt">${a}</div>
          <span class="conn">⇌</span>
          <div class="pt">${b}</div>
        </div>
        <div class="compat-score">${r.score}%</div>
        <div class="compat-label">${r.label}</div>
        <p class="compat-tip">${r.tip}</p>
        <div class="muted">${pa.nickname} ↔ ${pb.nickname}</div>
      `;
      const runs = (MBTI.Storage.get(MBTI.Storage.K.compatRuns, 0)) + 1;
      MBTI.Storage.set(MBTI.Storage.K.compatRuns, runs);
      MBTI.Gamification.addXP(20);
      if (runs >= 5) MBTI.Gamification.unlock('matchmaker');
    }
    function renderMatrix() {
      const wrap = document.getElementById('compat-matrix');
      const types = MBTI.Data.typeOrder;
      const cells = [];
      cells.push('<div class="mc head"></div>');
      types.forEach(t => cells.push(`<div class="mc head">${t}</div>`));
      types.forEach(row => {
        cells.push(`<div class="mc head">${row}</div>`);
        types.forEach(col => {
          const r = score(row, col);
          const a = (r.score - 35) / 63; // 0..1
          const bg = `hsla(${Math.round(260 - a * 200)},80%,${50 - a * 8}%,${0.18 + a * 0.55})`;
          cells.push(`<div class="mc" style="background:${bg}" title="${row} × ${col} — ${r.score}% (${r.label})">${r.score}</div>`);
        });
      });
      wrap.innerHTML = cells.join('');
    }
    return { show, score, topMatches, preset };
  })();

  /* =============================================================
     HISTORY
     ============================================================= */
  MBTI.History = (() => {
    function show() {
      MBTI.Gamification.render();
      const list = document.getElementById('history-list');
      const hist = MBTI.Storage.get(MBTI.Storage.K.history, []);
      if (!hist.length) {
        list.innerHTML = '<p class="history-empty">No past results yet — take the assessment to start your journey.</p>';
        return;
      }
      list.innerHTML = hist.map((h, i) => {
        const p = MBTI.Data.types[h.type] || { nickname: '' };
        const d = new Date(h.ts);
        return `<button class="history-row" data-i="${i}">
          <div>
            <div class="h-type">${h.type}</div>
            <div class="muted">${p.nickname}</div>
          </div>
          <div class="h-date">${d.toLocaleDateString()} ${d.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</div>
        </button>`;
      }).join('');
      list.onclick = (e) => {
        const r = e.target.closest('[data-i]');
        if (!r) return;
        const i = parseInt(r.dataset.i, 10);
        MBTI.Storage.set(MBTI.Storage.K.lastResult, hist[i]);
        MBTI.Router.go('results');
      };
    }
    return { show };
  })();

  /* =============================================================
     APP BOOTSTRAP
     ============================================================= */
  MBTI.App = {
    init() {
      MBTI.UI.initTheme();
      MBTI.UI.initSound();
      MBTI.Landing.render();
      MBTI.Types.init();
      MBTI.Gamification.render();
      MBTI.Router.init();
      // Mobile nav
      document.getElementById('nav-toggle').addEventListener('click', () => {
        document.querySelector('.nav').classList.toggle('open');
      });
      // Re-render radar when theme changes (next results show)
      // Lazy-init Chart deferred — when results view loads it'll exist.
    }
  };

  // Boot when DOM ready and deferred scripts loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => MBTI.App.init());
  } else {
    MBTI.App.init();
  }
})();
