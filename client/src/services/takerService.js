import api from '@/services/api';
import { headers } from '@/services/headers';

const takerService = {
  async fetchTakers(filter) {
    try {
      const params = { params: filter };
      const config = { ...headers(), ...params };
      const response = await api.get('takers/', config);
      return response;
    } catch (error) {
      console.error('Error fetching takers:', error);
      throw error;
    }
  },

  async postTaker(newTaker) {
    try {
      const response = await api.post('takers/', newTaker, headers());
      return response.data;
    } catch (error) {
      console.error('Error creating taker:', error);
      throw error;
    }
  },

  async removeTaker(takerId) {
    try {
      const response = await api.delete(`takers/${takerId}`, headers());
      return response.data;
    } catch (error) {
      console.error('Error removing taker:', error);
      throw error;
    }
  },

  async addDonate(donate) {
    try {
      const response = await api.post('donates/', donate, headers());
      return response.data;
    } catch (error) {
      console.error('Error adding donate:', error);
      throw error;
    }
  },

  async updateDonate(donate) {
    try {
      const response = await api.patch(`donates/${donate.id}/`, donate, headers());
      return response.data;
    } catch (error) {
      console.error('Error updating donate:', error);
      throw error;
    }
  },

  async stopDonate(takerId) {
    try {
      const response = await api.patch(`takers/${takerId}/stop_donate/`, null, headers());
      return response.data;
    } catch (error) {
      console.error('Error stopping donate:', error);
      throw error;
    }
  },

  async removeDonate(donateId) {
    try {
      const response = await api.delete(`donates/${donateId}`, headers());
      return response.data;
    } catch (error) {
      console.error('Error removing donate:', error);
      throw error;
    }
  }
};

export default takerService;
