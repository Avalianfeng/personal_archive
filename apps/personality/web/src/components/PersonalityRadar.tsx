import type { PersonalityVector, DimensionKey } from '@personal-archive/personality';
import { DIMENSION_LABELS, DIMENSION_CATEGORIES } from '@personal-archive/personality';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts';

interface PersonalityRadarProps {
  vector: PersonalityVector;
}

// 雷达图用到的维度子集（所有 15 维太密，分组展示或选高差异维度）
const RADAR_DIMS: DimensionKey[] = [
  'rationality', 'abstraction', 'planning', 'curiosity',
  'anxiety', 'empathy', 'emotionStability',
  'extraversion', 'independence', 'cooperation',
  'achievementDrive', 'securityDrive', 'freedomDrive',
  'ruleOrientation', 'fairness', 'loyalty',
];

export default function PersonalityRadar({ vector }: PersonalityRadarProps) {
  const data = RADAR_DIMS.map((dim) => ({
    dimension: DIMENSION_LABELS[dim],
    value: vector[dim] * 100,
  }));

  return (
    <div className="w-full h-80 mb-6">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="75%">
          <PolarGrid stroke="rgba(255,255,255,0.05)" />
          <PolarAngleAxis
            dataKey="dimension"
            tick={{ fill: '#8b9dc3', fontSize: 11 }}
          />
          <Radar
            name="人格向量"
            dataKey="value"
            stroke="#a78bfa"
            fill="#a78bfa"
            fillOpacity={0.15}
            strokeWidth={1.5}
            animationDuration={800}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
